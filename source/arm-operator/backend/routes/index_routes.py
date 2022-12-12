import requests
from backend.utils.request_utils import get_common_headers
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from global_variables import Config, db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("main.html")


@main.route("/client")
@login_required
def client():
    person_names = requests.get(
        f"{Config.IC_URI}/get_persons", headers=get_common_headers()
    ).json()["names"]
    auto_numbers = requests.get(
        f"{Config.IC_URI}/get_autos", headers=get_common_headers()
    ).json()["numbers"]

    return render_template(
        "client.html", name=current_user.login, faces=person_names, cars=auto_numbers
    )


@main.route("/video")
@login_required
def video():
    vs_names = requests.get(
        f"{Config.IC_URI}/get_video_streams", headers=get_common_headers()
    ).json()["names"]
    return render_template("video.html", streams=vs_names)
