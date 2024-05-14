import pytest
from models import User

def test_new_user():
    # with pytest.raises(BaseException):
    #     user = User(username="Ash")

    # with pytest.raises(BaseException):
    #     user = User(password="thestressedguy")

    user = User(username="Ash")
    assert user is not None

    user = User(username="Ash", password="thestressedguy")
    assert user is not None