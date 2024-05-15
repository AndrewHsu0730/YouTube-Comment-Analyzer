import pytest
from flask import Flask
from database import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User

# @pytest.fixture
# def invalid_user_1():
#     invalid_user = User(username="Ash")
#     return invalid_user

# @pytest.fixture
# def invalid_user_2():
#     invalid_user = User(password="thestressedguy")
#     return invalid_user

# @pytest.fixture
# def valid_user():
#     valid_user = User(username="Ash", password="thestressedguy")
#     return valid_user

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.instance_path = Path("./db").resolve()

    db.init_app(app)
    app.register_blueprint(auth_routes_bp, url_prefix="/")
    app.register_blueprint(html_routes_bp, url_prefix="/views")

    return app