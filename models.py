from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship,mapped_column
from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(100), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)
    videos = relationship('Video', back_populates='user', lazy=True)

class Video(db.Model):
    __tablename__ = 'video'
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255), nullable=False)
    url = mapped_column(String(255), nullable=False)
    views = mapped_column(Integer, nullable=False)
    likes = mapped_column(Integer, nullable=False)
    dislikes = mapped_column(Integer, nullable=False)
    word = mapped_column(Text, nullable=False)
    date = mapped_column(String(10), nullable=False)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='videos')