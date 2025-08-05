# Log-analyzer-

---

## Setup Instructions

### 1. Prerequisites

- Python 3.9+ and pip
- Node.js 18+ and npm
- (Optional) Docker + Docker Compose

---

## Local Development Setup

### Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Optional:
Set up a .env for Enviorment Vairables for:
SECRET_KEY
JWT_SECRET_KEY
UPLOAD_FOLDER
IN_DOCKER
FLASK_ENV

If no env variables are set up then it will default to a set up key for needed keys

# Run the Flask server
flask run

```
## Potential issues with Flask install:
There is an issue where is your env is missing some C extentions needed. If flask won't install correctly please try to use a conda env
```bash
conda create -n flask-env python=3.10
conda activate flask-env
pip install -r requirements.txt
```

### FrontEnd
```bash
cd ../frontend
npm install
npm run dev
```

## Docker Setup (Recommended)

```bash
docker-compose up --build
```

In Both Docker and Local deployment, uploaded files will be saved in <Log_Analyzer>/uploadedFolders


## Machine Learning: Anomaly Detection

For anomaly detection in log files, this project uses an **Isolation Forest** model.

### Why Isolation Forest?

Isolation Forest is designed to detect outliers by isolating anomalies rather than modeling normal data. It's well-suited for our case, where the vast majority of log entries are normal, and anomalies are more rare.

### How It Works

- The model builds a forest of random decision trees.
- Each tree randomly selects a feature and a split value to divide the data.
- Anomalous data points tend to be isolated **faster** (i.e., in fewer splits) than normal ones.
- The **average path length** across all trees is computed for each data point.
- Points with **shorter average path lengths** are flagged as anomalies.

### Feature Set

- `request_size`: The size of the request (numerical)
- `action`: The type of action (e.g., `"buy"`, `"sell"`, `"upload"`, `"download"`)
- `uaclass`: The client source (e.g., `"browser"`, `"curl"`)

### Example Anomaly Detection

A log entry may be flagged as anomalous if it has:

- A significantly **larger request size**
- An action like `"upload"` or `"download"`
- A client type like `"curl"`

Such a combination is unusual compared to regular traffic (e.g., small `buy/sell` requests from a browser), so the model assigns it a **higher anomaly score**.

The ML implemention is in the ML_detection File where we first preprocces the data to fit the model. Some features in our set are strings like action and uaclass are strings and not numerical values so we need to convert to numerical value using sklearn's `LabelEncoder()`.
My model is set up in the following way
```python 
model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42
    )
```
`n_estimators` is the number of isolation trees that will be created and split. Depending on the number of entries in the dataset we may want to incerease/decrease the number of trees. Typically increaseing will improve accuracy but decrease preformance but there is also a danger of overfitting
`contamination` is the percentage of how many anomolies we expect to be in the data. In a production model we would remove this parameters as we would use some saved training data
`random_state` is to keep reproducability based on the data set to get a consistant output on the same data set. In a production model we would remove this parameter as well 

---

