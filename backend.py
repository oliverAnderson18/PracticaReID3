from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/send", method=["POST"])
def send_message():
    return 0


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
