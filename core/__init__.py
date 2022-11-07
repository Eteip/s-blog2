from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# Database Setup
db = SQLAlchemy()
DB_NAME = "database.db" # Database name: database.db

# Create app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Importing the views, auth
    from .auth import auth
    from .views import views

    # Registering the views, auth
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    # User Model for login
    from .models import User

    # Create database Function passing app
    create_database(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Fetching the user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



#  Create database
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database!")
