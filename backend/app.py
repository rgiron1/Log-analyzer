from flask import Flask
from flask_cors import CORS
from upload import upload_bp
from analyze import analyze_bp
from dotenv import load_dotenv
import os
import logging 

app = Flask(__name__)
load_dotenv()

UPLOAD_FOLDER = r'C:\Users\rgiro\Log-analyzer\backend\uploadedFiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('SECRET_KEY')

# Register blueprints first
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)

# Then apply CORS after blueprints are registered
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)