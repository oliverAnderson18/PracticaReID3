from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import schemas
import users_db

users_bp = Blueprint("users", __name__)


@users_bp.route("/admin", methods=["POST"])
def store_admin():
    schema = schemas.LoginSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        if check_password_hash(users_db.users[username], password):
            users_db.users[username] = {
                "password": password,
                "is_admin": True
            }
            return jsonify({"Message": "Admin added correctly"}), 200
        else:
            return jsonify({"Error": "Password incorrect"}), 401

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400


@users_bp.route("/grant", methods=["PUT", "POST"])
def grant_admin():
    data = request.json
    user1 = data.get("user1")
    user2 = data.get("user2")

    if user1["is_admin"]:
        user2["is_admin"] = True
        return jsonify({"Message": f"User: {user2} is now an admin"}), 200
    else:
        return jsonify({"Error": f"User: {user2} can't be an admin"}), 404


@users_bp.route("/status/<username_id>", methods=["GET"])
def get_status(username_id):
    data = request.json
    data["username_id"] = username_id

    if users_db.users[username_id]:
        return users_db.users[username_id["is_admin"]], 200
    return jsonify({"Error": "Username not in database"}), 404
