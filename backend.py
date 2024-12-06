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
    data = request.json
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    uid = uuid.uuid4().hex
    db.messages[uid] = data["content"]
    print("Message stored:", db.messages)

    return jsonify({uid: data["content"]}), 200


@app.route("/messages", methods=["GET"])
def receive_message():
    schema = schemas.MessageSchema()

    try:
        schema.load({"content": "dummy"})
    except ValidationError as e:
        return jsonify({"Error": e.messages["content"]}), 404

    return jsonify(db.messages), 200


@app.route("/modify/<message_id>", methods=["PUT"])
def modify_resource(message_id):
    schema = schemas.ModifyMessageSchema()
    request_data = request.json
    print(request_data)
    request_data["message_id"] = message_id
    print(request_data)
    try:
        schema.load(request_data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    db.messages[message_id] = request_data["content"]
    return jsonify({message_id: db.messages[message_id]}), 200


@app.route("/delete/<message_id>", methods=["DELETE"])
def delete_resource(message_id):
    schema = schemas.DeleteMessageSchema()
    data = {"message_id": message_id}
    print(data)
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    del db.messages[message_id]
    return jsonify({"Message": "Deleted successfully"}), 200


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Modify endpoints for differente requests.</p>"""


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
