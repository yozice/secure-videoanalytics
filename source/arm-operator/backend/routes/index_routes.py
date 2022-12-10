from flask import Blueprint, render_template
from flask_login import current_user, login_required
from global_variables import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("main.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.login)
