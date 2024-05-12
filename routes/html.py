from flask import Flask, url_for, render_template, request, Blueprint, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,current_user

html_routes_bp = Blueprint("html", __name__)

@html_routes_bp.route("/home")
def home():
    print(current_user)
    return render_template("/html/home.html", user=current_user)

@html_routes_bp.route("/faq")
def faq():
    return render_template("/html/faq.html")

@html_routes_bp.route("/about")
def about():
    return render_template("/html/about.html")

@html_routes_bp.route("/contact")
def contact():
    return render_template("/html/contact.html")

@html_routes_bp.route("/privacy")
def privacy():
    return render_template("/html/privacy.html")

@html_routes_bp.route("/terms")
def terms():
    return render_template("/html/terms.html")