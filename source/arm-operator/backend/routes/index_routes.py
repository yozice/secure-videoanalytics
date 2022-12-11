from flask import Blueprint, render_template
from flask_login import current_user, login_required
from global_variables import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("main.html")


@main.route("/client")
@login_required
def client():
    return render_template("client.html", name=current_user.login)

@main.route("/video")
@login_required
def video():
    return render_template("video.html")
