import pytest
from models import User, Video, Comment
from database import db
from app import app
from manage import create_tables, drop_tables
from werkzeug.security import generate_password_hash
from datetime import datetime

def test_new_user():
    with app.app_context():
        with pytest.raises(TypeError):
            user = User(username="Ash")
            db.session.add()
            db.session.commit()

        with pytest.raises(TypeError):
            user = User(password="thestressedguy")
            db.session.add(user)
            db.session.commit()

        user = User(username="admin", password=generate_password_hash("admin123", method="pbkdf2"))
        db.session.add(user)
        db.session.commit()
        assert user is not None
        assert user.id == 4
        assert user.username == "admin"
        assert user.password != "admin123"

def test_video():
    with app.app_context():
        video = Video(title="Title", url="URL", views=1, likes=1, dislikes=1, score=0.18, word="Word", date=datetime.strptime("2024-5-15", "%Y-%m-%d"), user_id=1)
        db.session.add(video)
        db.session.commit()
        assert video is not None

def test_user_video_connection():
    with app.app_context():
        assert db.session.execute(db.select(User)).scalar().videos[0].title == "Title"

def test_comment():
    with app.app_context():
        comment = Comment(text="Text", video_id=1)
        db.session.add(comment)
        db.session.commit()
        assert comment is not None

def test_video_comment_connection():
    with app.app_context():
        assert db.session.execute(db.select(Video)).scalar().comments[0].text == "Text"
        drop_tables()
        create_tables()