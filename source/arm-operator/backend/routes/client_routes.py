import json

import requests
from backend.utils.request_utils import get_common_headers
from flask import Blueprint, jsonify, make_response, render_template, request
from flask_login import current_user, login_required
from global_variables import Config, db

client = Blueprint("client", __name__)


@client.route("/add_person", methods=["POST"])
@login_required
def add_person():
    posted_person_data = eval(request.form["person_data"])
    media = request.files["file"]
    resp = requests.post(
        f"{Config.IC_URI}/add_person",
        headers=get_common_headers(),
        files=[
            ("media", (media.filename, media.read(), "multipart/form-data")),
            (
                "person_data",
                ("person_data", json.dumps(posted_person_data), "application/json"),
            ),
        ],
    )
    if resp:
        return jsonify({"message": "successfully added person"}), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@client.route("/get_person_info/<name>", methods=["GET"])
@login_required
def get_person_info(name):
    resp = requests.get(
        f"{Config.IC_URI}/get_person_info/{name}",
        headers=get_common_headers(),
    )
    if resp:
        return jsonify(resp.json()), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@client.route("/rm_person/<id>", methods=["DELETE"])
@login_required
def rm_person(id):
    resp = requests.delete(
        f"{Config.IC_URI}/rm_person/{id}",
        headers=get_common_headers(),
    )
    if resp:
        return jsonify(resp.json()), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@client.route("/add_auto", methods=["POST"])
@login_required
def add_auto():
    data = request.get_json()
    resp = requests.post(
        f"{Config.IC_URI}/add_auto", headers=get_common_headers(), json=data
    )
    if resp:
        return jsonify({"message": resp.json()["message"]}), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@client.route("/get_auto_info/<number>", methods=["GET"])
@login_required
def get_auto_info(number):
    resp = requests.get(
        f"{Config.IC_URI}/get_auto_info/{number}",
        headers=get_common_headers(),
    )
    if resp:
        return jsonify(resp.json()), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@client.route("/rm_auto/<id>", methods=["DELETE"])
@login_required
def rm_auto(id):
    resp = requests.delete(
        f"{Config.IC_URI}/rm_auto/{id}",
        headers=get_common_headers(),
    )
    if resp:
        return jsonify(resp.json()), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)
