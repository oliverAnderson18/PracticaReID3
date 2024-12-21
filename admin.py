from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
import schemas
import users_db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/register", methods=["POST"])
def store_admin():
    schema = schemas.RegisterSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        passw = generate_password_hash(password)
        users_db.users[username] = {
            "password": passw,
            "is_admin": True
        }

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400

    return jsonify({"Message": f"{username} is now registered as an admin"}), 200


@admin_bp.route("/grant", methods=["PUT", "POST"])
def grant_admin():
    data = request.json
    user1 = data.get("user1")
    user2 = data.get("user2")

    if user1["is_admin"]:
        user2["is_admin"] = True
        return jsonify({"Message": f"User: {user2} is now an admin"}), 200
    else:
        return jsonify({"Error": f"User: {user2} can't be an admin"}), 404


@admin_bp.route("/status/<username_id>", methods=["GET"])
def get_status(username_id):
    data = request.json
    data["username_id"] = username_id

    if users_db.users[username_id]:
        return users_db.users[username_id["is_admin"]], 200
    return jsonify({"Error": "Username not in database"}), 404
