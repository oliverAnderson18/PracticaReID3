from flask import Flask
from flask_jwt_extended import JWTManager
import os
import datetime
from auth import auth_bp
from texts import texts_bp
from admin import admin_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
print(os.getenv("SECRET_KEY"))
print("SECRET_KEY configurado:", app.config["SECRET_KEY"])
app.config["SESSION_TYPE"] = "filesystem"
app.config["JWT_SESSION_TYPE"] = "JWT_SECRET_KEY"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=30)
jwt = JWTManager(app)


# Los blueprints de texts
app.register_blueprint(texts_bp, url_prefix="/texts")

# Los blueprints de auth
app.register_blueprint(auth_bp, url_prefix="/auth")

# Los blueprints de admin
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)
