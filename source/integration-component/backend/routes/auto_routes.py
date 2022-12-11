from backend.models import Detection
from backend.token import token_required
from flask import Blueprint, jsonify, make_response, request
from global_variables import db

detection_bp = Blueprint("detection", __name__)


@detection_bp.route("/add_detection", methods=["POST"])
@token_required
def add_detection():
    data = request.get_json()
    auto = Auto.query.filter_by(name=data["name"]).first()
    if not auto:
        new_auto = Auto(name=data["name"])
        db.session.add(new_auto)
        db.session.commit()
        return jsonify({"message": "registered successfully"}), 201
    else:
        return make_response(jsonify({"message": "auto already exists"}), 409)


@detection_bp.route("/get_autos", methods=["GET"])
@token_required
def get_autos():
    autos_meta = Auto.query.all()
    autos_numbers = [x.number for x in autos_meta]
    return jsonify({"names": autos_numbers})


@detection_bp.route("/get_auto_info/<auto_number>", methods=["GET"])
@token_required
def get_auto_info(auto_number):
    auto = Auto.query.filter_by(name=auto_number).first()
    if auto:
        return jsonify({"id": auto.id, "number": auto.number, "model": auto.model})
    else:
        return make_response(jsonify({"message": "auto does not exist"}), 409)


@detection_bp.route("/rm_auto", methods=["DELETE"])
@token_required
def rm_auto():
    data = request.get_json()
    auto = Auto.query.filter_by(id=int(data["id"])).delete()
    if auto:
        db.session.commit()
        return jsonify({"message": "successfully removed from database"}), 201
    else:
        return make_response(jsonify({"message": "auto does not exist"}), 409)
