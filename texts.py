from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import db
import uuid
import schemas

texts_bp = Blueprint("texts", __name__)


@texts_bp.route("/send", methods=["POST"])
@jwt_required()
def send_message():
    schema = schemas.SendMessageSchema()
    data = request.json

    try:
        schema.load(data)
        if get_jwt_identity():
            uid = uuid.uuid4().hex
            db.messages[uid] = {"content": data["content"], "ToGemini": False, "Response": None}
            print("Message stored:", db.messages)
            return jsonify({uid: {"content": data["content"], "ToGemini": False, "Response": None}}), 200
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404


@texts_bp.route("/messages", methods=["GET"])
@jwt_required()
def receive_message():
    if get_jwt_identity():
        schema = schemas.MessageSchema()
        try:
            schema.load({"content": "dummy"})
        except ValidationError as e:
            return jsonify({"Error": e.messages["content"]}), 404
        return jsonify(db.messages), 200
    else:
        return jsonify({"Error": "unauthorized token"}), 401


@texts_bp.route("/modify/<message_id>", methods=["PUT"])
@jwt_required()
def modify_resource(message_id):
    schema = schemas.ModifyMessageSchema()
    request_data = request.json
    request_data["message_id"] = message_id

    try:
        schema.load(request_data)
        if get_jwt_identity():
            db.messages[message_id]["content"] = request_data["content"]
            return jsonify({message_id: db.messages[message_id]["content"]}), 200
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404


@texts_bp.route("/delete/<message_id>", methods=["DELETE"])
@jwt_required()
def delete_resource(message_id):
    schema = schemas.DeleteMessageSchema()
    data = {"message_id": message_id}
    print(data)
    try:
        schema.load(data)
        if get_jwt_identity():
            del db.messages[message_id]
            return jsonify({"Message": "Deleted successfully"}), 200
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404
