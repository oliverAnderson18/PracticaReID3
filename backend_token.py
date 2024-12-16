import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
import db
import uuid
import schemas
import users_db
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=30)
jwt = JWTManager(app)


def generate_token(username):
    return create_access_token(identity=username)


def verify_token():
    return get_jwt_identity()


@app.route("/send", methods=["POST"])
@jwt_required()
def send_message():
    current_user = verify_token()
    schema = schemas.SendMessageSchema()
    data = request.json

    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    uid = uuid.uuid4().hex
    db.messages.append({"id": uid, "content": data["content"], "author": current_user})
    return jsonify({uid: data["content"]}), 200


@app.route("/messages", methods=["GET"])
@jwt_required()
def receive_message():
    return jsonify(db.messages), 200


@app.route("/modify/<message_id>", methods=["PUT"])
@jwt_required()
def modify_resource(message_id):
    current_user = verify_token()
    schema = schemas.ModifyMessageSchema()
    request_data = request.json
    request_data["message_id"] = message_id

    try:
        schema.load(request_data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    for message in db.messages:
        if message["id"] == message_id:
            if message["author"] != current_user:
                return jsonify({"Error": "Unauthorized modification attempt"}), 403
            message["content"] = request_data["content"]
            return jsonify({message_id: message["content"]}), 200

    return jsonify({"Error": "Message not found"}), 404


@app.route("/delete/<message_id>", methods=["DELETE"])
@jwt_required()
def delete_resource(message_id):
    current_user = verify_token()

    for i, message in enumerate(db.messages):
        if message["id"] == message_id:
            if message["author"] != current_user:
                return jsonify({"Error": "Unauthorized deletion attempt"}), 403
            del db.messages[i]
            return jsonify({"Message": "Deleted successfully"}), 200

    return jsonify({"Error": "Message not found"}), 404


@app.route("/register", methods=["POST"])
def create_user():
    schema = schemas.RegisterSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        schema.load(data)
        if username in users_db.users:
            return jsonify({"Error": "User already exists"}), 400
        users_db.users[username] = password
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400

    return jsonify({username: "registered successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    schema = schemas.LoginSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        schema.load(data)
        if users_db.users.get(username) == password:
            access_token = generate_token(username)
            return jsonify({"token": access_token}), 200
        else:
            return jsonify({"Error": "Invalid credentials"}), 401
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Endpoints secured with JWT.</p>"""


if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True)
