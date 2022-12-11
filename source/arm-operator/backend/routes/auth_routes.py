from backend.models import User
from flask import Blueprint, flash, redirect, render_template, request, url_for, get_flashed_messages
from flask_login import login_required, login_user, logout_user
from global_variables import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/auth")
def auth_page():
    return render_template('login.html')


@auth.route("/login", methods=["POST"])
def login_post():
    data = request.get_json()
    login = data['login']
    password = data['password']

    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(login=login).first()

    # check if the user actually exists
    if not user or not check_password_hash(user.password, password):
        return {'status': 'fail', 'message': 'Неправильный логин или пароль'}

    login_user(user, remember=remember)
    return {'status': 'ok', 'message': url_for("main.index")}

@auth.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()
    login = data['login']
    password = data['password']

    user = User.query.filter_by(login=login).first()
    if user:  # if user with this login already exists in db
        return {'status': 'fail', 'message': 'Пользователь с таким логином уже зарегистрирован'}

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        login=login,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return {'status': 'ok', 'message': url_for("main.index")}


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.auth_page"))
