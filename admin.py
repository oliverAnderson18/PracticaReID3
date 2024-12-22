from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
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
    user1 = data.get("username1") # Usuario admin
    user2 = data.get("username2")
    password1 = data.get("password1")
    user_data = users_db.users.get(user1)
    stored_password_hash = user_data.get("password")
    schema1 = schemas.UserAdmin()
    schema2 = schemas.StatusUser()
    try:
        schema1.load({"username": user1})
        schema2.load({"username": user2})
        if check_password_hash(stored_password_hash, password1):
            users_db.users[user2]["is_admin"] = True
            return jsonify({"Message": f"{user1} granted {user2} admin permissions"}), 200
        else:
            return jsonify({"Error": "Password incorrect"}), 401
    except:
        return jsonify({"Error": "Either one or both of users passwords are incorrect"}), 404


@admin_bp.route("/status/<username_id>", methods=["GET"])
def get_status(username_id):
    data = request.json
    data["username_id"] = username_id
    schema = schemas.StatusUser()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": "Username not in database"}), 404
    return users_db.users[username_id["is_admin"]], 200