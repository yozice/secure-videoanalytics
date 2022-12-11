import json

import requests
from backend.utils.request_utils import get_common_headers
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from global_variables import Config, db

client = Blueprint("client", __name__)


@client.route("/add_person", methods=["POST"])
@login_required
def add_person():
    # posted_person_data = json.load(request.files["person_data"])
    data = request.get_json()
    print(data)
    # for file in request.files:
    #     print(file)
    # resp = requests.post(
    #     Config.IC_URI,
    #     headers=get_common_headers(),
    # )
    return jsonify({"message": "successfully added person"}), 201


@client.route("/add_auto", methods=["POST"])
@login_required
def add_auto():
    data = request.get_json()
    print(data)
    return jsonify({"message": "successfully added auto"}), 201
