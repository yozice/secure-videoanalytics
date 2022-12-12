import hashlib
import json

from backend.models import FaceImage, Person
from backend.token import token_required
from backend.utils import image_utils
from flask import Blueprint, jsonify, make_response, request
from global_variables import db

person_bp = Blueprint("person", __name__)


@person_bp.route("/add_person", methods=["POST"])
@token_required
def add_person():
    # image_utils.save_byte_img(request.files["media"].read(), "./imgs/img.jpg")
    posted_person_data = json.load(request.files["person_data"])
    person = Person.query.filter_by(name=posted_person_data["name"]).first()
    if not person:
        # adding to person
        new_person = Person(name=posted_person_data["name"])
        db.session.add(new_person)

        # adding to faceimages
        if request.files:
            face_images = []
            for request_filename in request.files:
                file = request.files[request_filename]
                if file.content_type == "multipart/form-data":
                    total_images = FaceImage.query.count()
                    filename = f"{total_images}.jpg"
                    face_image = FaceImage(filename=filename, person_id=new_person.id)
                    image_utils.save_byte_img(file.read(), f"./facebank/{filename}")
                    face_images.append(face_image)
            for face_image in face_images:
                db.session.add(face_image)

        # commit
        db.session.commit()

        # передать в видеоаналитику
        return jsonify({"message": "registered successfully"}), 201
    else:
        return make_response(jsonify({"message": "person already exists"}), 409)


@person_bp.route("/get_persons", methods=["GET"])
@token_required
def get_persons():
    persons_meta = Person.query.all()
    persons_names = [x.name for x in persons_meta]
    return jsonify({"names": persons_names})


@person_bp.route("/get_person_info/<person_name>", methods=["GET"])
@token_required
def get_person_info(person_name):
    person = Person.query.filter_by(name=person_name).first()
    if person:
        return jsonify({"id": person.id, "name": person.name})
    else:
        return make_response(jsonify({"message": "person does not exist"}), 409)


@person_bp.route("/rm_person/<id>", methods=["DELETE"])
@token_required
def rm_person(id):
    data = request.get_json()
    person = Person.query.filter_by(id=int(id)).delete()
    if person:
        db.session.commit()
        return jsonify({"message": "successfully removed from database"}), 201
    else:
        return make_response(jsonify({"message": "person does not exist"}), 409)
