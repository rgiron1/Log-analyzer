import os
from flask import Flask, Blueprint, jsonify, current_app
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route("/analyze/<filename>", methods=["GET"])
def analyze_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER'] #file path to store uploaded files
    filepath = os.path.join(upload_folder, filename)
    if not os.path.exists(filepath):
        return jsonify({"success": False, "error": "File not found"}), 404

    parsed_data = parse_log_file(filepath)
    return jsonify({"success": True} | parsed_data), 200

def parse_log_file(filepath):
    # Dummy parser: count lines & first 5 lines preview
    with open(filepath, "r") as f:
        lines = f.readlines()
    return {
        "total_lines": len(lines),
        "preview": lines[:5]
    }