from flask import url_for, render_template, request, Blueprint, redirect, session
from database import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

auth_routes_bp = Blueprint("authorization", __name__)


@auth_routes_bp.route("/")
def home():
    return render_template("/auth/login.html")


@auth_routes_bp.route("/auth/register")
def register():
    return render_template("/auth/signup.html")


@auth_routes_bp.route("/auth/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    # remember = True if request.form.get("remember") else False
    statement = db.select(User).where(User.username == username)
    user = db.session.execute(statement).scalar()
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for("authorization.home"))
    login_user(user)
    return redirect(url_for("html.home"))

@auth_routes_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("authorization.home"))

@auth_routes_bp.route("/auth/register", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    if not username or not password:
        return redirect(url_for("authorization.register"))
    if username == "" or password == "":
        return redirect(url_for("authorization.register"))
    new_user = User(username = username, password = generate_password_hash(password, method="scrypt"))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("authorization.home"))