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
    user1 = data.get("username1")
    user2 = data.get("username2")
    password1 = data.get("password1")
    password2 = data.get("password2")

    if check_password_hash(users_db.users[user1]["password"], password1) and check_password_hash(users_db.users[user2]["password"],
                                                                                                 password2):
        if users_db.users[user1]["is_admin"]:
            users_db.users[user2]["is_admin"] = True
            return jsonify({"Message": f"{user1} granted {user2} admin permissions"}), 200
        else:
            return jsonify({"Error": f"{user1} must be an admin to grant admin permission"}), 404
    else:
        return jsonify({"Error": "Either one or both of users passwords are incorrect"}), 404


@admin_bp.route("/status/<username_id>", methods=["GET"])
def get_status(username_id):
    data = request.json
    data["username_id"] = username_id

    if users_db.users[username_id]:
        return users_db.users[username_id["is_admin"]], 200
    return jsonify({"Error": "Username not in database"}), 404


# The next function is used to check out a users password only by an admin

@admin_bp.route("/checkout-password", methods=["GET"])
def checkout_password():
    data = request.json
    user1 = data.get("username1")
    user2 = data.get("username2")
    password1 = data.get("password1")

    if check_password_hash(users_db.users[user1]["password"], password1):
        if users_db.users[user1]["is_admin"]:
            return jsonify({"Message": f"{user2} password is: {users_db.users[user2]["password"]}"}), 200
        else:
            return jsonify({"Error": f"{user1} must be an admin to check out {user2}'s password"}), 404
    else:
        return jsonify({"Error": "The password is incorrect"}), 404
