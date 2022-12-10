from backend.models import User
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from global_variables import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template('login.html')


@auth.route("/login", methods=["POST"])
def login_post():
    login = request.form.get("login")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(login=login).first()

    # check if the user actually exists
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template('signup.html')


@auth.route("/signup", methods=["POST"])
def signup_post():
    login = request.form.get("login")
    password = request.form.get("password")

    user = User.query.filter_by(login=login).first()

    if user:  # if user with this login already exists in db
        flash("Email address already exists")
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
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
