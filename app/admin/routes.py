from flask import render_template
from flask_login import login_required, current_user
from app.admin import admin_bp

@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    return render_template(
        "admin/dashboard.html"
    )