from flask import Flask
from flask_cors import CORS
from upload import upload_bp
from analyze import analyze_bp
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from auth import auth_bp
import os
import logging 

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY') or 'fallback-secret-key'
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  or 'fallback-secret-key'# use env var in production
JWTManager(app)
app.register_blueprint(auth_bp)

# Check if running in Docker
IN_DOCKER = os.getenv("IN_DOCKER") == "true"

# Set upload folder based on environment
if IN_DOCKER:
    UPLOAD_FOLDER = "/app/uploads"
else:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploadedFiles")

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)

CORS(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)