from datetime import datetime

from backend.models import Auto, Detection, Person
from backend.token import token_required
from flask import Blueprint, jsonify, make_response, request
from global_variables import db

detection_bp = Blueprint("detection", __name__)


@detection_bp.route("/add_detection", methods=["POST"])
@token_required
def add_detection():
    data = request.get_json()
    for prediction in data["predictions"]:
        new_detection = Detection(
            timestamp=datetime.strptime(data["timestamp"], "%d/%m/%y %H:%M:%S"),
            prediction=prediction["bbox"],
            stream_id=int(data["stream_id"]),
        )
        if prediction["type"] == "face":
            person = Person.query.filterby(name=prediction["label"]).first()
            new_detection.person_id = person.id
        else:
            auto = Auto.query.filterby(name=prediction["label"]).first()
            new_detection.auto_id = auto.id
        db.session.add(new_detection)
    db.session.commit()
    return jsonify({"message": "registered successfully"}), 201
