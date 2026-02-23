from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "Zoho-setu-secret-2026"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

users = {}

# Welcome route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Zoho Setu App!"})


# Register
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password") or not data.get("email"):
        return jsonify({"error": "username, email & password are required!"}), 400

    username = data["username"]
    email = data["email"]
    password = data["password"]

    if username in users:
        return jsonify({"error": "Username already taken!"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    users[username] = {
        "username": username,
        "email": email,
        "password": hashed_password
    }

    return jsonify({"message": f"User '{username}' registered successfully!"}), 201


# Login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username and password are required!"}), 400

    username = data["username"]
    password = data["password"]

    if username not in users:
        return jsonify({"error": "Invalid username or password!"}), 401

    stored_user = users[username]

    if not bcrypt.check_password_hash(stored_user["password"], password):
        return jsonify({"error": "Invalid username or password!"}), 401

    token = create_access_token(identity=username)

    return jsonify({
        "message": "Login successful!",
        "token": token,
        "username": username
    }), 200


# Profile (Protected)
@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user_data = users[current_user]

    return jsonify({
        "username": user_data["username"],
        "email": user_data["email"],
        "message": "You are logged in!"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)