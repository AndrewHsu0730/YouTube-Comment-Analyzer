from flask import Flask, url_for, render_template, request, Blueprint, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from analyzer import *
import os

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

@html_routes_bp.route("/dashboard", methods = ["POST"])
def read_url():
    url = request.form["url"]
    pages = request.form["pages"]
    vid = urlToVid(url)
    word_comments,comments = getComment(vid, pages) # Process comments
    print(word_comments)
    wc = generateWordCloud(word_comments) # Generate word cloud
    wc.savefig(os.path.join("static", "images", "word_cloud.png")) # Save the word cloud
    sentimentDict = calculateScore(comments)
    pie_chart = getPieChart(sentimentDict) # Generate pie chart
    pie_chart.savefig(os.path.join("static", "images", "pie_chart.png")) # Save the pie chart
    return render_template("/html/dashboard.html")