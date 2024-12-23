from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import schemas
import users_db

admin_bp = Blueprint("admin", __name__)



@admin_bp.route("/grant", methods=["PUT", "POST"])
@jwt_required()
def grant_admin():
    data = request.json
    admin_user = get_jwt_identity()

    user = data.get("username")
    schema1 = schemas.UserAdmin()
    schema2 = schemas.StatusUser()
    try:
        schema1.load({"username": admin_user})
    except ValidationError as e:
        return jsonify({"Error": f"{admin_user} is not admin"}), 403
    try:
        schema2.load({"username": user})
        users_db.users[user]["is_admin"] = True
        return jsonify({"Message": f"{admin_user} granted {user} admin permissions"}), 200
    except ValidationError as e:
        return jsonify({"Error": f"{user} not in database"}), 404


@admin_bp.route("/status/<username_id>", methods=["GET"])
@jwt_required()
def get_status(username_id):
    admin_user = get_jwt_identity()
    schema1 = schemas.UserAdmin()
    try:
        schema1.load({"username": admin_user})
    except ValidationError as e:
        return jsonify({"Error": f"{admin_user} is not admin"}), 403
    
    schema = schemas.StatusUser()
    try:
        schema.load({"username": username_id})
    except ValidationError as e:
        return jsonify({"Error": "Username not in database"}), 404
    return jsonify({username_id: users_db.users[username_id]["is_admin"]}), 200