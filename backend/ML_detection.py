import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define features the model expects
FEATURE_COLUMNS = ["reqsize", "actions", "uaclass"]
CATEGORICAL_COLS = ["actions", "uaclass"]

# Encoders are trained per batch (assumes categorical values are consistent)

def preprocess(rows):
    encoders = {col: LabelEncoder() for col in CATEGORICAL_COLS}
    col_values = {col: [] for col in CATEGORICAL_COLS}

    # Gather all categorical values to fit encoders
    for row in rows:
        for col in CATEGORICAL_COLS:
            col_values[col].append(row.get(col, "unknown"))

    for col in CATEGORICAL_COLS:
        encoders[col].fit(col_values[col])

    X = []
    valid_indices = []

    for idx, row in enumerate(rows):
        try:
            reqsize_str = row.get("reqsize", 0)
            try:
                reqsize = float(reqsize_str)
            except ValueError:
                logger.warning(f"Invalid reqsize for row {idx}: {reqsize_str}")
                continue

            features = [reqsize]
            logger.info(f"Processing reqsize: {reqsize}")

            for col in CATEGORICAL_COLS:
                val = row.get(col, "unknown")
                encoded = float(encoders[col].transform([val])[0])
                features.append(encoded)

            X.append(features)
            valid_indices.append(idx)

        except Exception as e:
            logger.warning(f"Skipping row {idx} due to error: {e}, row: {row}")
            continue

    return np.array(X), valid_indices

def run_model_on_logs(log_rows):

    X, valid_indices = preprocess(log_rows)

    if len(X) == 0:
        return [], [], []

    logger.info(f"Sample size: {len(X)} — unique rows: {len(np.unique(X, axis=0))}")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42
    )
    model.fit(X)

    raw_scores = model.decision_function(X)  # higher = more normal
    predictions = model.predict(X)           # -1 = anomaly

    anomalies = [False] * len(log_rows)
    scores = [0.0] * len(log_rows)
    confidence = [0.0] * len(log_rows)

    min_score = np.min(raw_scores)
    max_score = np.max(raw_scores)
    score_range = max_score - min_score if max_score != min_score else 1.0

    for i, idx in enumerate(valid_indices):
        is_anomaly = predictions[i] == -1
        score = float(raw_scores[i])
        norm_score = (score - min_score) / score_range
        reqsize_value = X[i][0]

        anomalies[idx] = is_anomaly
        scores[idx] = score
        confidence[idx] = norm_score

        log_rows[idx]["reqsize"] = reqsize_value
        log_rows[idx]["model_score"] = score
        log_rows[idx]["confidence_score"] = norm_score
        log_rows[idx]["anomaly"] = is_anomaly

    return anomalies, scores, confidence
