from flask import Blueprint
from global_variables import db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "Login"


@auth.route("/signup")
def signup():
    return "Signup"


@auth.route("/logout")
def logout():
    return "Logout"
