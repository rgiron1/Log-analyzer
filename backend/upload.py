import os
from flask import Flask, Blueprint, flash, jsonify, request, redirect, current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
import logging

ALLOWED_EXTENSIONS = {'txt', 'log'} #allowed file extensions

app = Flask(__name__)
CORS(app) 
upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 #16MB limit for file uploads


def allowed_file(filename): #check if the file has an allowed extension
    logger.info("Checking if file is allowed: %s", filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_if_name_exists(filename):#check if a file with the same name already exists in the upload folder
    logger.info("Checking if file already exist: %s", filename)
    return os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash('File is too large. Maximum upload size is 16MB.')
    logger.error("File too large")
    return jsonify({"success": False, "error": "File too large"}), 400

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if 'file' not in request.files: #if no file part in the request
        flash('No file part')
        logger.error("No file part in the request")
        return jsonify({"success": False, "error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '': #if no file is selected
        flash('No selected file')
        logger.error("No selected file")
        return jsonify({"success": False, "error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        if check_if_name_exists(file.filename):
            flash('File with this name already exists. Please rename the file and try again.')
            logger.error("File with this name already exists: %s", file.filename)
            return jsonify({"success": False, "error": "File with this name already exists. Please rename the file and try again."}), 400
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        flash(f"File {filename} uploaded successfully!")
        logger.info("File has been successfully uploaded!")
        return jsonify({"success": True, "filename": filename}), 201
    
    flash('File type not allowed. Please upload a .txt or .log file.')
    logger.error("File type not allowed: %s", file.filename)
    return jsonify({"success": False, "error": "File type not allowed, please upload a .txt or .log file"}), 400

@upload_bp.route("/upload/<filename>", methods=["GET"])
def get_uploaded_file(filename):
    # if not allowed_file(filename):
    #     return jsonify({"success": False, "error": "File type not allowed"}), 400
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        logger.error("File not found: %s", file_path)
        return jsonify({"success": False, "error": "File not found", "FilePath": file_path}), 404
    logger.info("File has been found: %s", file_path)
    return jsonify({"success": True, "filename": filename}), 200