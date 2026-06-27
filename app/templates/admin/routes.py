from flask import render_template

from flask_login import (
    login_required,
    current_user
)

from app.admin import admin_bp

from app.models import (
    User,
    Trek,
    Booking
)


@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "ADMIN":

        return "Unauthorized",403

    return render_template(

        "admin/dashboard.html",

        total_treks=Trek.query.count(),

        total_users=User.query.filter_by(
            role="TREKKER"
        ).count(),

        total_staff=User.query.filter_by(
            role="STAFF"
        ).count(),

        total_bookings=Booking.query.count()

    )