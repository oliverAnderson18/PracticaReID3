from flask import Flask
from flask import request, jsonify
from db import messages
import uuid

app = Flask(__name__)


@app.route("/send", method=["POST"])
def send_message(messages):
    data = request.json
    if not data or "content" not in data:
        return jsonify({"Error": "Content is required"}), 400

    uid = uuid.uuid4().hex
    messages[uid] = data["content"]
    return jsonify({uid: data["content"]}), 200


@app.route("/receive", method=["GET"])
def receive_message():
    return 0


@app.route("/modify", method=["PUT"])
def modify_resource():
    return 0


@app.route("/delete", method=["DELETE"])
def delete_resource():
    return 0


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
