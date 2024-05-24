from flask_login import LoginManager
from models import User
from app import app
from database import db
from werkzeug.security import generate_password_hash
from manage import *

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

    def test_login_logic():
        with app.app_context():
            drop_tables()
            create_tables()
            user = User(username="user1", password=generate_password_hash("user111", method="sha512"))
            db.session.add(user)
            db.session.commit()
            response = test_client.post("/auth/login", data={"username": "user1", "password": "user111"}, follow_redirects=True)
            assert response.status_code == 200

    def test_home_page():
        with app.app_context():
            user = User(username="user2", password=generate_password_hash("user222", method="sha512"))
            db.session.add(user)
            db.session.commit()
            response = test_client.post("/auth/login", data={"username": "user2", "password": "user222"}, follow_redirects=True)
            assert b"Video URL" in response.data

    def test_dashboard():
        with app.app_context():
            user = User(username="user3", password=generate_password_hash("user333", method="sha512"))
            db.session.add(user)
            db.session.commit()
            response = test_client.post("/auth/login", data={"username": "user3", "password": "user333"}, follow_redirects=True)
            response = test_client.post("/views/dashboard", data={"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "pages": 1}, follow_redirects=True)
            assert b"Dashboard" in response.data

    def test_other_pages():
        with app.app_context():
            user = User(username="user4", password=generate_password_hash("user444", method="sha512"))
            db.session.add(user)
            db.session.commit()
            response = test_client.post("/auth/login", data={"username": "user4", "password": "user444"}, follow_redirects=True)
            response = test_client.get("views/about")
            assert b'<img\n    src="/static/images/InsightForge.png"\n    alt="Insight Forge logo for YouTube Comment Analyzer"\n  />' in response.data
            response = test_client.get("/views/terms")
            assert b"Terms And Conditions" in response.data