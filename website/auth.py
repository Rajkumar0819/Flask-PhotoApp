from flask import render_template, Blueprint, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.images_page'))

            else:
                flash("Incorrect Password", category='error')

        else:
            flash("Email does not exist", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email Already exist", category='error')
        elif len(email) < 4:  # type: ignore
            flash("Email must be greater than 4 characters", category="error")
        elif len(first_name) < 2:  # type: ignore
            flash("Name must be at least 4 characters", category="error")
        elif password1 != password2:
            flash("Entered password incorrectly type again", category="error")
        elif len(password1) < 7:  # type: ignore
            flash("password length must be at least 7 characters", category="error")
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='scrypt'),
                            first_name=first_name)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash("Account Created Successfully!!!", category="success")
            return redirect(url_for("views.images_page"))
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html")
