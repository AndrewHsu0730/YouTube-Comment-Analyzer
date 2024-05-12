from flask import Flask, render_template, request
from database import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User
import os
from analyzer import *

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path("./db").resolve()

db.init_app(app)
app.register_blueprint(auth_routes_bp, url_prefix="/")
app.register_blueprint(html_routes_bp, url_prefix="/views")
login_manager = LoginManager()
login_manager.login_view = "authorization.home"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods = ["POST"])
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

if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port=8008)