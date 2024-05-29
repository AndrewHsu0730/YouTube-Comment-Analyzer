from flask import app, render_template, request, Blueprint, url_for
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
    user = current_user           
    url = request.form["url"]
    pages = request.form["pages"]
    
    vid = urlToVid(url)
    global title
    title = getTitle(vid)
    thumbnail = getThumbnail(vid)
    
    like_count, dislike_count, view_count = getStat(vid) #Fetch data from returndislike API
    word_comments,comments = getComment(vid, pages) # Process comments
    

    if  word_comments or comments:
        most_occured_word = max(word_comments, key=word_comments.get) #Get mosr common word in 
        sentimentDict, avg_score = calculateScore(comments)
        new_video(current_user.id,getTitle(vid),url,view_count,like_count,dislike_count,avg_score,most_occured_word)
        retrieveData(current_user.id,url)
        getAllChart(word_comments,sentimentDict)
    else:
        new_video(current_user.id,getTitle(vid),url,view_count,like_count,dislike_count, 0, "Not Avaliable")
        retrieveData(current_user.id,url)
        return render_template("/html/dashboard.html" ,title = title,error = True, thumbnail = thumbnail, user=user)
    return render_template("/html/dashboard.html" ,title = title, thumbnail = thumbnail, user=user)