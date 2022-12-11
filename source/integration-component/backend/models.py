from dataclasses import dataclass
from datetime import datetime

from global_variables import db


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    component_name = db.Column(db.String(200))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    face_images = db.relationship("FaceImage", backref="person", lazy=True)
    logins = db.relationship("Detection", backref="person", lazy=True)


class FaceImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)


class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    model = db.Column(db.String(20))
    logins = db.relationship("Detection", backref="auto", lazy=True)


class VideoStream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    url = db.Column(db.String(200))
    port = db.Column(db.String(200))
    detections = db.relationship("Detection", backref="video_stream", lazy=True)


class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    prediction = db.Column(db.String(300))
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=True)
    auto_id = db.Column(db.Integer, db.ForeignKey("auto.id"), nullable=True)
    video_stream_id = db.Column(
        db.Integer, db.ForeignKey("video_stream.id"), nullable=False
    )
