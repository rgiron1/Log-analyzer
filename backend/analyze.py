import os
from flask import Flask, Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
import logging
import csv
from ML_detection import run_model_on_logs

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
analyze_bp = Blueprint('analyze', __name__)



@analyze_bp.route("/analyze/<filename>", methods=["GET"])
@jwt_required()
def analyze_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER'] #File path to store uploaded files
    filepath = os.path.join(upload_folder, filename)
    if not os.path.exists(filepath):
        logger.error("File not found: %s", filepath)
        return jsonify({"success": False, "error": "File not found"}), 404

    table_data = []
    summary = {
        "total_entries": 0,
        "high_risk_count": 0,
        "critical_risk_count": 0,
        "average_request_size": 0,
        "top_urls": {},
        "top_users": {},
        "timeline": []
    }

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile) # Use DictReader to read CSV as dictionaries since headers are present
        for row in reader:
            table_data.append(row)
            summary['total_entries'] += 1

            severity = row.get("threatseverity", "None")
            timestamp = row.get("timestamp", "unknown")
            url = row.get("url", "unknown")
            user = row.get("login", "unknown")
            country = row.get("srcip_country", "unknown")
            method = row.get("reqmethod", "unknown")
            respcode = row.get("respcode", "unknown")
            ipAddress = row.get("cpubip", "unknown")
            request_size = row.get("reqsize", "0")
            uaclasses = row.get("uaclass", "unknown")
            actions = row.get("action", "unknown")
            activity = row.get("activity", "unknown")

            if severity == "High":
                summary["high_risk_count"] += 1
            elif severity == "Critical":
                summary["critical_risk_count"] += 1

            summary["timeline"].append({
                "timestamp": timestamp,
                "severity": severity,
                "user": user,
                "url": url,
                "country": country,
                "method": method,
                "response_code": respcode,
                "ip_address": ipAddress,
                "reqsize": request_size,
                "uaclass": uaclasses,
                "actions": actions,
                "activity": activity
            })

            # Top URLs
            summary["top_urls"].setdefault(url, 0)
            summary["top_urls"][url] += 1

            # Top users
            summary["top_users"].setdefault(user, 0)
            summary["top_users"][user] += 1

            # Calculate average request size
            request_size = float(request_size)
            if request_size > 0:  # Avoid division by zero
                summary["average_request_size"] += request_size

        # Sort top URLs and users by count
        if summary["total_entries"] > 0:
            summary["average_request_size"] /= summary["total_entries"]
        else:
            summary["average_request_size"] = 0
        logger.info("Sorting top URLs and users and Timeline")
        summary["top_urls"] = dict(sorted(summary["top_urls"].items(), key=lambda item: item[1], reverse=True))
        summary["top_users"] = dict(sorted(summary["top_users"].items(), key=lambda item: item[1], reverse=True))
        summary["timeline"].sort(key=lambda x: x["timestamp"])
        anomalies, scores, confidence = run_model_on_logs(summary["timeline"])
        for i, entry in enumerate(summary["timeline"]):
            entry["anomaly"] = bool(anomalies[i])
            entry["confidence_score"] = round(confidence[i], 4)
            entry["model_score"] = round(scores[i], 4)
            


    logger.info("File has been successfully analyzed")
    return jsonify({
        "success": True,
        "table": table_data,
        "summary": summary
    }), 200


