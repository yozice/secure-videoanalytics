from flask_login import UserMixin
from global_variables import db


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # name = db.Column(db.String(1000))
