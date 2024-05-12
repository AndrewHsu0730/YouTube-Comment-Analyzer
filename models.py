from sqlalchemy import Numeric, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import mapped_column, relationship
from database import db
from flask_login import UserMixin


class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(100), unique=True, nullable=False)
    videos = db.relationship('Video', back_populates='user', lazy=True)

class Video(db.Model):
    id = mapped_column(Integer, primary_key=True)
    video_id = mapped_column(String(50), unique=True, nullable=False)
    title = mapped_column(String(255), nullable=False)
    url = mapped_column(String(255), nullable=False)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='videos')
    comments = db.relationship('Comment', back_populates='video', lazy=True)

class Comment(db.Model):
    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(Text, nullable=False)
    video_id = mapped_column(Integer, ForeignKey('video.id'), nullable=False)
    video = db.relationship('Video', back_populates='comments')
    created_at = mapped_column(DateTime, nullable=False, default=DateTime.utcnow)
