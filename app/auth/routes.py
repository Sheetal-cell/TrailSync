from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import (
    login_user,
    logout_user,
    login_required
)
from app.auth import auth_bp
from app.auth.forms import (
    RegistrationForm,
    LoginForm
)
from app.extensions import db
from app.models import User
from app.utils.security import (
    hash_password,
    verify_password
)

# -----------------------------
# Login
# -----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    from flask_login import current_user

    if current_user.is_authenticated:

        if current_user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == "STAFF":
            return redirect(url_for("staff.dashboard"))

        return redirect(url_for("trekker.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        # User not found
        if not user:
            flash(
                "Invalid email or password.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )
        # Password check
        if not verify_password(
            user.password,
            form.password.data
        ):
            flash(
                "Invalid email or password.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )
        # Blacklisted / Deactivated account
        if not user.is_active:
            flash(
                "Your account has been deactivated by the administrator.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )
        # Staff approval check
        if (
            user.role == "STAFF"
            and user.status != "APPROVED"
        ):
            flash(
                "Your account is awaiting admin approval.",
                "warning"
            )
            return redirect(
                url_for("auth.login")
            )

        # Login successful
        login_user(user)

        flash(
            f"Welcome back, {user.full_name}!",
            "success"
        )
        # Redirect based on role
        if user.role == "ADMIN":
            return redirect(
                url_for("admin.dashboard")
            )
        elif user.role == "STAFF":
            return redirect(
                url_for("staff.dashboard")
            )
        elif user.role == "TREKKER":
            return redirect(url_for("trekker.dashboard"))

        return redirect(url_for("auth.login"))
    return render_template(
        "auth/login.html",
        form=form
    )

# -----------------------------
# Register
# -----------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    from flask_login import current_user

    if current_user.is_authenticated:

        if current_user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == "STAFF":
            return redirect(url_for("staff.dashboard"))

        return redirect(url_for("trekker.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "danger"
            )
            return redirect(
                url_for("auth.register")
            )
        # Staff require admin approval
        status = (
            "PENDING"
            if form.role.data == "STAFF"
            else "APPROVED"
        )
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hash_password(
                form.password.data
            ),
            role=form.role.data,
            status=status
        )
        db.session.add(new_user)
        db.session.commit()
        if form.role.data == "STAFF":
            flash(
                "Registration successful! Your account is awaiting admin approval.",
                "info"
            )
        else:
            flash(
                "Registration successful! Please login to continue.",
                "success"
            )
        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "auth/register.html",
        form=form
    )

# -----------------------------
# Logout
# -----------------------------
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    flash(
        "Logged out successfully.",
        "success"
    )
    return redirect(
        url_for("auth.login")
    )