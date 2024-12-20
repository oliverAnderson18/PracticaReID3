from flask import Flask, session
from flask import request, jsonify
from flask_session import Session
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import db
import uuid
import schemas
import users_db
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
print(os.getenv("SECRET_KEY"))
print("SECRET_KEY configurado:", app.config["SECRET_KEY"])
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/send", methods=["POST"])
def send_message():
    print("Headers:", request.headers)
    print("JSON Data:", request.json)

    data = request.json
    schema = schemas.SendMessageSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404

    uid = uuid.uuid4().hex
    db.messages[uid] = {"content": data["content"]}
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
    request_data = request.json
    request_data["message_id"] = message_id
    schema = schemas.ModifyMessageSchema()
    try:
        schema.load(request_data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404
    db.messages[message_id]["content"] = request_data["content"]
    return jsonify({message_id: db.messages[message_id]["content"]}), 200


@app.route("/delete/<message_id>", methods=["DELETE"])
def delete_resource(message_id):
    data = {"message_id": message_id}
    schema = schemas.DeleteMessageSchema()
    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 404
    del db.messages[message_id]
    return jsonify({"Message": "Deleted successfully"}), 200


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
def get_users():
    schema = schemas.UserSchema()
    try:
        schema.load({"content": "dummy"})
    except ValidationError as e:
        return jsonify({"Error": "User database empty"}), 404
    
    return jsonify(users_db.users), 200


@app.route("/login", methods=["POST"])
def generate_cookie():
    schema = schemas.LoginSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        schema.load(data)
        if check_password_hash(users_db.users[username], password):
            session["username"] = username
            session["logged_in"] = True
            if session.get("logged_in"):
                return jsonify({"Success": f"Hello, {session['username']}! You have logged in correctly"}), 200
        else:
            return jsonify({"Error": "password incorrect"}), 401

    except ValidationError as e:
        return jsonify({"Error": e.messages}), 401


@app.route("/logout", methods=["DELETE", "POST"])
def delete_user():
    schema = schemas.LogoutSchema()
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        schema.load(data)
        if check_password_hash(users_db.users[username], password):
            session.pop("username", None)
            session.clear()
            if not session.get("logged_in"):
                return jsonify({"Exito": "Session ended"}), 200
            
        else:
            return jsonify({"Error": "password incorrect"}), 401

    except ValidationError as e:
        return jsonify({"Error": "Credentials incorrect"}), 401


@app.route("/get_session", methods=["GET"])
def get_session():
    return jsonify({"session_content": dict(session)})


@app.route("/")
def index():
    return """<h1>Message Application</h1><p>Modify endpoints for different requests.</p>"""


if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True) 
    