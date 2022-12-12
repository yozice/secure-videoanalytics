import os

from dotenv import load_dotenv
from flask import Flask

import routes

load_dotenv()


def create_app():
    """
    Entry point to the Flask Server application.
    """
    app = Flask(
        __name__, static_folder="frontend/static", template_folder="frontend/templates"
    )
    app.secret_key = "secret"

    app.register_blueprint(routes.app)

    return app


if __name__ == "__main__":
    app = create_app()
