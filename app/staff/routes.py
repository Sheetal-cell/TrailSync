
from flask import render_template
from flask_login import login_required, current_user
from app.staff import staff_bp

@staff_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "STAFF":
        return "Unauthorized", 403

    return render_template(
        "staff/dashboard.html"
    )