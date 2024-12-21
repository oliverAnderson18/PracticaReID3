from flask import Flask, session
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
import db
import uuid
import schemas
import users_db
import os
import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
print(os.getenv("SECRET_KEY"))
print("SECRET_KEY configurado:", app.config["SECRET_KEY"])
app.config["SESSION_TYPE"] = "filesystem"
app.config["JWT_SESSION_TYPE"] = "JWT_SECRET_KEY"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=30)
jwt = JWTManager(app)



@app.route("/send", methods=["POST"])
@jwt_required()
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
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404


@app.route("/messages", methods=["GET"])
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

@app.route("/modify/<message_id>", methods=["PUT"])
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


@app.route("/delete/<message_id>", methods=["DELETE"])
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
    

@app.route("/register", methods=["POST"])
def create_user():
    schema = schemas.RegisterSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        passw = generate_password_hash(password)
        users_db.users[username] = passw
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400

    return jsonify({username: password}), 200


@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    schema = schemas.UserSchema()
    try:
        schema.load({"content": "dummy"})
        if get_jwt_identity():
            return jsonify(users_db.users), 200
        else:
            return jsonify({"Error": "unauthorized token"}), 401
    except ValidationError as e:
        return jsonify({"Error": "User database empty"}), 404


@app.route("/login", methods=["POST"])
def generate_token():
    schema = schemas.LoginSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        schema.load(data)
        if check_password_hash(users_db.users[username], password):
            access_token = create_access_token(identity=username)
            return jsonify({"Access Token": access_token}), 200
        else:
            return jsonify({"Error": "Password incorrect"}), 401

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Modify endpoints for different requests.</p>"""


if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True)