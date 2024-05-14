import pytest
from models import User, Video
from database import db
from app import app 

def test_new_user():
    with pytest.raises(TypeError):
        user = User(username="Ash")

    with pytest.raises(TypeError):
        user = User(password="thestressedguy")

    user = User(username="Ash", password="thestressedguy")
    assert user is not None

def test_video():
    video = Video(title="Title", url="URL", user_id=1)
    assert video is not None

def test_user_video_connection():
    with app.app_context():
        user = User(username="homie", password="thestressedguy")
        db.session.add(user)
        db.session.commit()
        assert (user.id) == 4