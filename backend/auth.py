from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

#in a production environment, you would store these securely, e.g., in a database
#for this example, I use a simple dictionary to simulate user storage
users = {
    "admin": generate_password_hash("Welcome1"),
}

@auth_bp.route("/verifyJWT", methods=["GET"])# check if the JWT is valid
@jwt_required()
def verify_token():
    return jsonify({"valid": True}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=username, expires_delta=timedelta(hours=.25))  # Token expires in 15 minutes
    return jsonify(access_token=token)
