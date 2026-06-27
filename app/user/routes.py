from flask import render_template
from flask_login import login_required, current_user
from app.user import user_bp


@user_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    return render_template(
        "user/dashboard.html"
    )