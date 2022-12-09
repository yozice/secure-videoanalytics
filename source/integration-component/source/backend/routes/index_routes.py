from flask import Blueprint
from global_variables import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return "Index"


@main.route("/profile")
def profile():
    return "Profile"
