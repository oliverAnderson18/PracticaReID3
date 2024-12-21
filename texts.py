from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
import db
import uuid
import schemas

users_bp = Blueprint("users", __name__)


@users_bp.route("/send", methods=["POST"])
def send_message():
    schema = schemas.SendMessageSchema()
    data = request.json

    try:
        schema.load(data)
        if get_jwt_identity():
            uid = uuid.uuid4().hex
            db.messages[uid] = {"content": data["content"]}
            print("Message stored:", db.messages)
            return jsonify({uid: data["content"]}), 200
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404


@users_bp.route("/messages", methods=["GET"])
def receive_message():
    if get_jwt_identity():
        schema = schemas.MessageSchema()
        try:
            schema.load({"content": "dummy"})
        except ValidationError as e:
            return jsonify({"Error": e.messages["content"]}), 404
        return jsonify(db.messages), 200


@users_bp.route("/modify/<message_id>", methods=["PUT"])
def modify_resource(message_id):
    schema = schemas.ModifyMessageSchema()
    request_data = request.json
    request_data["message_id"] = message_id

    try:
        schema.load(request_data)
        if get_jwt_identity():
            db.messages[message_id]["content"] = request_data["content"]
            return jsonify({message_id: db.messages[message_id]["content"]}), 200

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404


@users_bp.route("/modify/<message_id>", methods=["DELETE"])
def delete_resource(message_id):
    schema = schemas.DeleteMessageSchema()
    data = {"message_id": message_id}
    print(data)
    try:
        schema.load(data)
        if get_jwt_identity():
            del db.messages[message_id]
            return jsonify({"Message": "Deleted successfully"}), 200
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404
