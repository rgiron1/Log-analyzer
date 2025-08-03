import os
import uuid
from datetime import datetime, timezone
from flask import Flask, Blueprint, flash, jsonify, request, redirect, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import logging

ALLOWED_EXTENSIONS = {'txt', 'log', 'csv'} #allowed file extensions

app = Flask(__name__)
upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 #16MB limit for file uploads


def allowed_file(filename): #check if the file has an allowed extension
    logger.info("Checking if file is allowed: %s", filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash('File is too large. Maximum upload size is 16MB.')
    logger.error("File too large")
    return jsonify({"success": False, "error": "File too large"}), 400

@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if 'file' not in request.files: #if no file part in the request
        flash('No file part')
        logger.error("No file part in the request")
        return jsonify({"success": False, "error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '': #if no file is selected
        logger.error("No selected file")
        return jsonify({"success": False, "error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        orginal_filename = secure_filename(file.filename)
        name, ext = os.path.splitext(orginal_filename)
        unique_id = str(uuid.uuid4())[:8]  # Generate a unique ID
        filename = f"{name}_{unique_id}{ext}"  # Append unique ID to the filename
        file.save(os.path.join(upload_folder, filename))
        filesize_bytes = len(file.read())  # Get the size of the file
        upload_time = datetime.now(timezone.utc).isoformat()  # Get the current time
        file_metadata = {
            "success":True,
            "file_id": unique_id,
            "saved_filename": filename,
            "original_filename": orginal_filename,
            "file_size": filesize_bytes,
            "upload_time": upload_time,
            "extension": ext}
        logger.info("File has been successfully uploaded!")
        return jsonify(file_metadata), 201
    
    flash('File type not allowed. Please upload a .txt or .log file.')
    logger.error("File type not allowed: %s", file.filename)
    return jsonify({"success": False, "error": "File type not allowed, please upload a .txt or .log file"}), 400

@upload_bp.route("/upload/<filename>", methods=["GET"])
@jwt_required()
def get_uploaded_file(filename):
    # if not allowed_file(filename):
    #     return jsonify({"success": False, "error": "File type not allowed"}), 400
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        logger.error("File not found: %s", file_path)
        return jsonify({"success": False, "error": "File not found", "FilePath": file_path}), 404
    logger.info("File has been found: %s", file_path)
    return jsonify({"success": True, "filename": filename}), 200