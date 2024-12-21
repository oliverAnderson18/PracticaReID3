from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import schemas
import users_db

users_bp = Blueprint("users", __name__)


@users_bp.route("/login", methods=["POST"])
def login():
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


@users_bp.route("/register", methods=["POST"])
def register():
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
