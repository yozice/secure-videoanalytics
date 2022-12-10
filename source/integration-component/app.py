import os

from flask import Flask

from backend.routes import gate_control_routes, video_analytics_routes


def app_setup(app: Flask):
    """
    Entry point to the Flask Server application.
    """
    app.secret_key = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    video_analytics_routes.init_app(app)
    gate_control_routes.init_app(app)

    return app


app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)
app_setup(app)
