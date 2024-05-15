from conftest import create_app
from flask_login import LoginManager
from models import User

app = create_app()

login_manager = LoginManager()
login_manager.login_view = "authorization.home"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.test_client() as test_client:
    def test_landing_page():
        response = test_client.get("localhost:8008/")
        assert response.status_code == 200