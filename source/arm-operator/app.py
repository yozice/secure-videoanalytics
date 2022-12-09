import os

from flask import Flask

from backend.routes import auth_routes, index_routes
from global_variables import db


def app_setup(app: Flask):
    """
    Entry point to the Flask Server application.
    """
    app.secret_key = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

    db.init_app(app)

    app.register_blueprint(index_routes.main)
    app.register_blueprint(auth_routes.auth)
    return app


app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)
app_setup(app)
