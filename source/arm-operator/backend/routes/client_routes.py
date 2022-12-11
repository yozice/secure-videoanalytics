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
    # resp = requests.post(
    #     Config.IC_URI,
    #     headers=get_common_headers(),
    # )
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


@client.route("/add_auto", methods=["POST"])
@login_required
def add_auto():
    data = request.get_json()
    print(data)
    return jsonify({"message": "successfully added auto"}), 201
