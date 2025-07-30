from flask import Flask
from upload import upload_bp
from analyze import analyze_bp
from dotenv import load_dotenv
import os 

#file path to store uploaded files
UPLOAD_FOLDER = r'C:\Users\rgiro\Log-analyzer\backend\uploadedFiles'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)

if __name__ == "__main__":
    app.run(debug=True)
