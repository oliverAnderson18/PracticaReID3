from flask import Flask
from flask import request, jsonify
import db
import uuid
import schemas

app = Flask(__name__)


@app.route("/send", methods=["POST"])
def send_message():
    print("Headers:", request.headers)
    print("JSON Data:", request.json)

    data = request.json
    if not data or "content" not in data:
        return jsonify({"Error": "Content is required"}), 400

    uid = uuid.uuid4().hex
    db.messages[uid] = data["content"]
    print("Message stored:", db.messages)
    return jsonify({uid: data["content"]}), 200


@app.route("/messages", methods=["GET"])
def receive_message():
    try:
        message = schemas.MessageSchema()
    except ValueError as err:
        return jsonify(err), 404
    return jsonify(db.messages), 200


@app.route("/modify/<message_id>", methods=["PUT"])
def modify_resource(message_id):
    if message_id not in db.messages:
        return jsonify({"Error": "Message not found"}), 404

    data = request.json
    if not data or "content" not in data:
        return jsonify({"Error": "Content is required"}), 400

    db.messages[message_id] = data["content"]
    return jsonify({message_id: db.messages[message_id]}), 200



@app.route("/delete/<message_id>", methods=["DELETE"])
def delete_resource(message_id):
    if message_id not in db.messages:
        return jsonify({"Error": "Message not found"}), 404

    del db.messages[message_id]
    return jsonify({"Message": "Deleted successfully"}), 200


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Modify endpoints for differente requests.</p>"""


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
