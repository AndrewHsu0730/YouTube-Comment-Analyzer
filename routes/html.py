from flask import render_template, request, Blueprint, session
from flask_login import login_required, current_user
from analyzer import *
from datetime import datetime

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
    from manage import new_video
    from models import User,Video
    date = datetime.now().strftime("%Y-%m-%d %H:%M")                             
    url = request.form["url"]
    pages = request.form["pages"]
    vid = urlToVid(url)
    like_count, dislike_count, view_count = getStat(vid)
    title,word_comments,comments = getComment(vid, pages) # Process comments
    print(current_user)
    most_occured_word = max(word_comments, key=word_comments.get)
    new_video(current_user.id,title,url,view_count,like_count,dislike_count,most_occured_word,date)
    wc = generateWordCloud(word_comments) # Generate word cloud
    wc.savefig(os.path.join("static", "images", "word_cloud.png")) # Save the word cloud
    sentimentDict = calculateScore(comments)
    pie_chart = getPieChart(sentimentDict) # Generate pie chart
    pie_chart.savefig(os.path.join("static", "images", "pie_chart.png")) # Save the pie chart
    videos_with_same_url = Video.query.filter_by(url=url,user_id =current_user.id).all()
    dates_list = [video.date for video in videos_with_same_url]
    likes_list = [video.likes for video in videos_with_same_url]
    dislikes_list = [video.dislikes for video in videos_with_same_url]
    views_list = [video.views for video in videos_with_same_url]
    stats = getStats(dates_list,likes_list,dislikes_list,views_list)
    stats.savefig(os.path.join("static", "images", "stats.png"))
    return render_template("/html/dashboard.html")