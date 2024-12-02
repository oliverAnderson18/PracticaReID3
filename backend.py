from flask import Flask
from flask import request, jsonify
from db import messages
import uuid

app = Flask(__name__)


@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"Error": "Content is required"}), 400

    uid = uuid.uuid4().hex
    messages[uid] = data["content"]
    return jsonify({uid: data["content"]}), 200


@app.route("/receive/<message_id>", methods=["GET"])
def receive_message(message_id):
    if message_id not in messages:
        return jsonify({"Error": "Message not found"}), 404

    return jsonify({message_id: messages[message_id]}), 200


@app.route("/modify/<message_id>", methods=["PUT"])
def modify_resource(message_id):
    if message_id not in messages:
        return jsonify({"Error": "Message not found"}), 404

    data = request.json
    if not data or "content" not in data:
        return jsonify({"Error": "Content is required"}), 400

    messages[message_id] = data["content"]
    return jsonify({message_id: messages[message_id]}), 200


@app.route("/delete", methods=["DELETE"])
def delete_resource(message_id):
    if message_id not in messages:
        return jsonify({"Error": "Message not found"}), 404

    del messages[message_id]
    return jsonify({"Message": "Deleted successfully"}), 200


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
