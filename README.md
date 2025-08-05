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

```bash
docker-compose up --build
```

In Both Docker and Local deployment, uploaded files will be saved in <Log_Analyzer>/uploadedFolders


## Machine Learning: Anomaly Detection

For anomaly detection in log files, this project uses an **Isolation Forest** model.

### Why Isolation Forest?

Isolation Forest is designed to detect outliers by isolating anomalies rather than modeling normal data. It's well-suited for our case, where the vast majority of log entries are normal, and anomalies are rare.

### How It Works

- The model builds a forest of random decision trees.
- Each tree randomly selects a feature and a split value to divide the data.
- Anomalous data points tend to be isolated **faster** (i.e., in fewer splits) than normal ones.
- The **average path length** across all trees is computed for each data point.
- Points with **shorter average path lengths** are flagged as anomalies.

### Feature Set

We train the model using only clean (normal) logs. The feature set includes:

- `request_size`: The size of the request (numerical)
- `action_type`: The type of action (e.g., `"buy"`, `"sell"`, `"upload"`, `"download"`)
- `client_type`: The client source (e.g., `"browser"`, `"curl"`)

### Example Anomaly Detection

A log entry may be flagged as anomalous if it has:

- A significantly **larger request size**
- An action like `"upload"` or `"download"`
- A client type like `"curl"`

Such a combination is unusual compared to regular traffic (e.g., small `buy/sell` requests from a browser), so the model assigns it a **higher anomaly score**.

---

