from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    videos = relationship('Video', back_populates='user', lazy=True)

class Video(db.Model):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    views = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    dislikes = Column(Integer, nullable=False)
    word = Column(Text, nullable=False)
    date = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='videos')