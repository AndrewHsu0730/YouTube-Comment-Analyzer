from models import User

def test_new_user():
    user = User(username="Ash", password="thestressedguy")
    assert user.username == "Ash"
    # assert user.password == "thestressedguy"