from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from analyzer import *


html_routes_bp = Blueprint("html", __name__)

@html_routes_bp.route("/home")
@login_required
def home():
    return render_template("/html/home.html", user=current_user)

@html_routes_bp.route("/tutorial")
@login_required
def tutorial():
    return render_template("/html/tutorial.html")

@html_routes_bp.route("/dashboard", methods = ["POST"])

def read_url():
    from manage import new_video
    user = current_user           
    url = request.form["url"]
    pages = request.form["pages"]
    
    vid = urlToVid(url)

    if not vid:
        return redirect(url_for("html.home"))

    global title
    title = getTitle(vid)

    if not title:
        return redirect(url_for("html.home"))

    thumbnail = getThumbnail(vid)
    
    like_count, dislike_count, view_count = getStat(vid) # Fetch data from returndislike API
    word_comments, comments = getComment(vid, pages) # Process comments
    

    if word_comments or comments:
        most_occured_word = max(word_comments, key = word_comments.get) # Get most common word
        sentimentDict, avg_score = calculateScore(comments)
        new_video(current_user.id, getTitle(vid), url, view_count, like_count, dislike_count, avg_score, most_occured_word)
        retrieveData(current_user.id, url)
        latest_videos = getLatestVideos(current_user.id)
        getAllChart(word_comments, sentimentDict)
    else:
        new_video(current_user.id, getTitle(vid), url, view_count, like_count, dislike_count, 0, "Not Avaliable")
        retrieveData(current_user.id, url)
        latest_videos = getLatestVideos(current_user.id)
        return render_template("/html/dashboard.html", title = title, error = True, thumbnail = thumbnail, user = user, videos = latest_videos)
    return render_template("/html/dashboard.html", title = title, thumbnail = thumbnail, user = user, videos = latest_videos)