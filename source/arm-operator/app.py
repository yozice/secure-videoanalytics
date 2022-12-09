import os

from flask import Flask
from flask_login import LoginManager

from backend.models import User
from backend.routes import auth_routes, index_routes
from global_variables import db


def app_setup(app: Flask):
    """
    Entry point to the Flask Server application.
    """
    app.secret_key = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(index_routes.main)
    app.register_blueprint(auth_routes.auth)
    return app


app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)
app_setup(app)
