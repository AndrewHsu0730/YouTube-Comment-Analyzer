from sqlalchemy import Numeric, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import mapped_column
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(100), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)
    videos = db.relationship('Video', back_populates='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='scrypt')

class Video(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255), nullable=False)
    url = mapped_column(String(255), nullable=False)
    views = mapped_column(Integer, nullable=False)
    likes = mapped_column(Integer, nullable=False)
    dislikes = mapped_column(Integer, nullable=False)
    date = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='videos')
    comments = db.relationship('Comment', back_populates='video', lazy=True)

    def __init__(self, title, url, views, likes, dislikes, date, user_id):
        self.title = title
        self.url = url
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.user_id = user_id

class Comment(db.Model):
    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(Text, nullable=False)
    video_id = mapped_column(Integer, ForeignKey('video.id'), nullable=False)
    video = db.relationship('Video', back_populates='comments')

    def __init__(self, text, video_id):
        self.text = text
        self.video_id = video_id