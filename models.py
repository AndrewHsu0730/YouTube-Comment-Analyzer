from sqlalchemy import Numeric, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, mapped_column
from database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(100), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)
    videos = relationship('Video', back_populates='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Video(db.Model):
    __tablename__ = 'video'
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255), nullable=False)
    url = mapped_column(String(255), nullable=False)
    views = mapped_column(Integer, nullable=False)
    likes = mapped_column(Integer, nullable=False)
    dislikes = mapped_column(Integer, nullable=False)
    word = mapped_column(Text, nullable=False)
    date = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='videos')
    comments = relationship('Comment', back_populates='video', lazy=True)

    def __init__(self, title, url, views, likes, dislikes, word, date, user_id):
        self.title = title
        self.url = url
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.word = word
        self.date = date
        self.user_id = user_id

class Comment(db.Model):
    __tablename__ = "comment"
    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(Text, nullable=False)
    video_id = mapped_column(Integer, ForeignKey('video.id'), nullable=False)
    video = relationship('Video', back_populates='comments')

    def __init__(self, text, video_id):
        self.text = text
        self.video_id = video_id