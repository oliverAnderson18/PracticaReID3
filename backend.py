from flask import Flask
from flask import request, jsonify
from marshmallow import ValidationError
import db
import uuid
import schemas

app = Flask(__name__)


@app.route("/send", methods=["POST"])
def send_message():
    print("Headers:", request.headers)
    print("JSON Data:", request.json)

    schema = schemas.SendMessageSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400

    uid = uuid.uuid4().hex
    db.messages[uid] = data["content"]
    print("Message stored:", db.messages)

    return jsonify({uid: data["content"]}), 200


@app.route("/messages", methods=["GET"])
def receive_message():
    schema = schemas.MessageSchema()

    try:
        schema.load({"content": "dummy", "id": uuid.uuid4()})
    except ValidationError as e:
        return jsonify({"Error": e.messages["content"]}), 404

    return jsonify(db.messages), 200


@app.route("/modify/<message_id>", methods=["PUT"])
def modify_resource(message_id):
    schema = schemas.ModifyMessageSchema()

    request_data = request.json
    request_data["message_id"] = message_id

    try:
        data = schema.load(request_data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    db.messages[message_id] = data["content"]
    return jsonify({message_id: db.messages[message_id]}), 200


def delete_resource(message_id):
    schema = schemas.DeleteMessageSchema()

    try:
        schema.load({"id": message_id})
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    del db.messages[message_id]
    return jsonify({"Message": "Deleted successfully"}), 200


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Modify endpoints for differente requests.</p>"""


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
