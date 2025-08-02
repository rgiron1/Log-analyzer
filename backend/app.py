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
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # use env var in production
JWTManager(app)
app.register_blueprint(auth_bp)

UPLOAD_FOLDER = r'C:\Users\rgiro\Log-analyzer\backend\uploadedFiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register blueprints first
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)

# Then apply CORS after blueprints are registered
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)