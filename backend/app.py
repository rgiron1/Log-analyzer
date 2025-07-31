from flask import Flask
from flask_cors import CORS
from upload import upload_bp
from analyze import analyze_bp
from dotenv import load_dotenv
import os
import logging 

app = Flask(__name__)
CORS(app) 
#file path to store uploaded files
UPLOAD_FOLDER = r'C:\Users\rgiro\Log-analyzer\backend\uploadedFiles'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)

if __name__ == "__main__":
    app.run(debug=True)
