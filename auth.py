from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import schemas
import users_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def generate_token():
    schema = schemas.LoginSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user_data = users_db.users.get(username)
    stored_password_hash = user_data.get("password")
    try:
        schema.load(data)
        if check_password_hash(stored_password_hash, password):
            access_token = create_access_token(identity=username)
            return jsonify({"Access Token": access_token}), 200
        else:
            return jsonify({"Error": "Password incorrect"}), 401

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400


@auth_bp.route("/register", methods=["POST"])
def create_user():
    schema = schemas.RegisterSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        passw = generate_password_hash(password)
        users_db.users[username] = {
            "password": passw,
            "is_admin": False
        }
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400

    return jsonify({username: password}), 200


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    schema = schemas.UserSchema()
    try:
        schema.load({"content": "dummy"})
        if get_jwt_identity():
            return jsonify(users_db.users), 200
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError:
        return jsonify({"Error": "User database empty"}), 404


