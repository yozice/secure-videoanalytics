import os

from flask import Flask

from backend.routes import (
    auth_routes,
    gate_control_routes,
    index_routes,
    video_analytics_routes,
)
from global_variables import db


def app_setup(app: Flask):
    """
    Entry point to the Flask Server application.
    """
    app.secret_key = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    video_analytics_routes.init_app(app)
    gate_control_routes.init_app(app)

    app.register_blueprint(index_routes.main)
    app.register_blueprint(auth_routes.auth)
    return app


app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)
app_setup(app)
