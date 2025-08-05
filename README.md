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

### FrontEnd
```bash
cd ../frontend
npm install
npm run dev
```

## Docker Setup (Recommended)

docker-compose up --build

In Both Docker and Local deployment, uploaded files will be saved in <Log_Analyzer>/uploadedFolders

