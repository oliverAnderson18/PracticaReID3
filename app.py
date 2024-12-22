from flask import Flask
from admin import admin_bp
from auth import auth_bp
from texts import texts_bp
from flask_jwt_extended import JWTManager
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

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(texts_bp, url_prefix='/texts')


if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True)