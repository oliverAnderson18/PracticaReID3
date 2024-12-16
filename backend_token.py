from flask import Flask, session
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
import db
import uuid
import schemas
import users_db
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
print(os.getenv("SECRET_KEY"))
print("SECRET_KEY configurado:", app.config["SECRET_KEY"])
app.config["SESSION_TYPE"] = "filesystem"
app.config["JWT_SESSION_TYPE"] = "JWT_SECRET_KEY"
jwt = JWTManager(app)


@app.route("/register", methods=["POST"])
def create_user():
    schema = schemas.RegisterSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        passw = generate_password_hash(password)
        users_db.users[username] = passw
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400

    return jsonify({username: password}), 200


@app.route("/users", methods=["GET"])
def get_users():
    schema = schemas.UserSchema()
    try:
        schema.load({"content": "dummy"})
    except ValidationError as e:
        return jsonify({"Error": "User database empty"}), 404

    return jsonify(users_db.users), 200


@app.route("/login", methods=["POST"])
@jwt_required()
def generate_token():
    schema = schemas.LoginSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        if check_password_hash(users_db.users[username], password):
            access_token = create_access_token(identity=username)
            return jsonify({"Access Token": access_token}), 200
        else:
            return jsonify({"Error": "Password incorrect"}), 401

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Modify endpoints for different requests.</p>"""


if __name__ == "_main_":
    app.run("127.0.0.1", port=5000, debug=True)