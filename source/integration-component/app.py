import os

from backend.routes import (
    auto_routes,
    detection_routes,
    person_routes,
    video_analytics_routes,
    video_stream_routes,
)
from config import app_config
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from global_variables import db

load_dotenv()

config_name = os.getenv("FLASK_ENV", "default")


app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)
app.config.from_object(app_config[config_name])

db.init_app(app)

app.register_blueprint(video_analytics_routes.video_analytics)
app.register_blueprint(person_routes.person_bp)
app.register_blueprint(auto_routes.detection_bp)
app.register_blueprint(video_stream_routes.video_stream_bp)
app.register_blueprint(detection_routes.detection_bp)


@app.before_first_request
def create_tables():
    db.create_all()


migrate = Migrate(app, db, render_as_batch=True)  # obj for db migrations
CORS(app)
