from flask_login import LoginManager
from models import User
from app import app
from database import db

login_manager = LoginManager()
login_manager.login_view = "authorization.home"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.test_client() as test_client:
    def test_login_page():
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Don't have an account?" in response.data

    def test_signup_page():
        response = test_client.get("/auth/register")
        assert response.status_code == 200
        assert b"Already have an account?" in response.data

    def test_redirect():
        response = test_client.get("/views/home")
        assert response.status_code == 302

    # def test_login_logic():
    #     with app.app_context():
    #         user = User(username="Aquarium", password="aquarium123")
    #         db.session.add(user)
    #         db.session.commit()
    #         response = test_client.post("/auth/login", data={"username": "Aquarium", "password": "aquarium123"})
    #         assert b""

    # def test_home_page():
    #     pass