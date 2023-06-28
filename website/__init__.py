from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import os

db = SQLAlchemy()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "33b880df130214c5b63b9c43bb1886ca18307a73"
    app.config['SQLALCHEMY_DATABASE_URI'] = rf"sqlite:///{DB_PATH}"

    db.init_app(app)

    from .models import User, Image
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists(DB_PATH):
        with app.app_context():
            db.create_all()

