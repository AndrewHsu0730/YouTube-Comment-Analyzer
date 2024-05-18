from flask import Flask
from database import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path("./db").resolve()

db.init_app(app)
app.register_blueprint(auth_routes_bp, url_prefix="/")
app.register_blueprint(html_routes_bp, url_prefix="/views")
login_manager = LoginManager()
login_manager.login_view = "authorization.home"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port=8008)
    
 