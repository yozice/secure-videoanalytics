from backend.models import User
from flask import Blueprint, redirect, request, url_for
from global_variables import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "Login"  # render_template('login.html')


@auth.route("/signup")
def signup():
    return "Signup"  # render_template('signup.html')


@auth.route("/signup", methods=["POST"])
def signup_post():
    login = request.form.get("login")
    password = request.form.get("password")

    user = User.query.filter_by(login=login).first()

    if user:  # if user with this login already exists in db
        return redirect(url_for("auth.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        login=login,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@auth.route("/logout")
def logout():
    return "Logout"
