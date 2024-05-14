from flask import Flask, url_for, render_template, request, Blueprint, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from analyzer import *
import os

html_routes_bp = Blueprint("html", __name__)

@html_routes_bp.route("/home")
@login_required
def home():
    print(current_user)
    return render_template("/html/home.html", user=current_user)

@html_routes_bp.route("/faq")
@login_required
def faq():
    return render_template("/html/faq.html")

@html_routes_bp.route("/about")
@login_required
def about():
    return render_template("/html/about.html")

@html_routes_bp.route("/contact")
@login_required
def contact():
    return render_template("/html/contact.html")

@html_routes_bp.route("/privacy")
@login_required
def privacy():
    return render_template("/html/privacy.html")

@html_routes_bp.route("/terms")
@login_required
def terms():
    return render_template("/html/terms.html")

@html_routes_bp.route("/dashboard", methods = ["POST"])
def read_url():
    url = request.form["url"]
    pages = request.form["pages"]
    vid = urlToVid(url)
    word_comments,comments = getComment(vid, pages) # Process comments
    wc = generateWordCloud(word_comments) # Generate word cloud
    wc.savefig(os.path.join("static", "images", "word_cloud.png")) # Save the word cloud
    sentimentDict = calculateScore(comments)
    print(sentimentDict)
    pie_chart = getPieChart(sentimentDict) # Generate pie chart
    pie_chart.savefig(os.path.join("static", "images", "pie_chart.png")) # Save the pie chart
    bar_chart = getBarChart(sentimentDict) # Generate bar chart
    bar_chart.savefig(os.path.join("static", "images", "bar_chart.png")) # Save the bar chart
    common_chart = getCommonChart(word_comments) # Generate pie chart
    common_chart.savefig(os.path.join("static", "images", "common_chart.png")) # Save the pie chart
    return render_template("/html/dashboard.html")


@html_routes_bp.route("/select" , methods=['GET', 'POST'])
def select():
    images = [
        {'url': url_for('static', filename='images/pie_chart.png'), 'value': 'pie_chart'},
        {'url': url_for('static', filename='images/bar_chart.png'), 'value': 'bar_chart'},
        {'url': url_for('static', filename='images/common_chart.png'), 'value': 'common_chart'}
    ]

    selected_image_url = images[0]['url'] 
    if request.method == 'POST':
        selected_value = request.form['image']
        for image in images:
            if image['value'] == selected_value:
                selected_image_url = image['url']
                break

    return render_template('/html/dashboard.html', images=images, selected_image_url=selected_image_url)
