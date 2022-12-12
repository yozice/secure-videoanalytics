import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Config:
    IC_URI = os.environ.get("IC_URI")
    IC_TOKEN = os.environ.get("IC_TOKEN")
