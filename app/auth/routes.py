from flask import render_template
from app.auth import auth_bp
from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from app.auth.forms import (
    RegistrationForm,
    LoginForm
)
from app.models import User
from app.extensions import db
from app.utils.security import (
    hash_password,
    verify_password
)
from flask_login import (
    login_user,
    logout_user
)
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if not user:
            flash(
                "Invalid credentials.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )
        if not verify_password(
            user.password,
            form.password.data
        ):
            flash(
                "Invalid credentials.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )

        if user.role == "STAFF":
            if user.status != "APPROVED":
                flash(
                    "Your account is awaiting admin approval.",
                    "warning"
                )
                return redirect(
                    url_for("auth.login")
                )
        login_user(user)

        if user.role == "ADMIN":
            return redirect("/admin")

        elif user.role == "STAFF":
            return redirect("/staff")

        return redirect("/user")

    return render_template(
        "auth/login.html",
        form=form
    )

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            flash(
                "Email already exists.",
                "danger"
            )
            return redirect(
                url_for("auth.register")
            )
        status = (
            "PENDING"
            if form.role.data == "STAFF"
            else "APPROVED"
        )
        user = User(

            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hash_password(
                form.password.data
            ),
            role=form.role.data,
            status=status
        )

        db.session.add(user)
        db.session.commit()
        flash(
            "Registration Successful!",
            "success"
        )
        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "auth/register.html",
        form=form
    )

@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect("/")