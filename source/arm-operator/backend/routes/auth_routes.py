from flask import Blueprint
from global_variables import db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "Login"  # render_template('login.html')


@auth.route("/signup")
def signup():
    return "Signup"  # render_template('signup.html')


@auth.route("/logout")
def logout():
    return "Logout"
