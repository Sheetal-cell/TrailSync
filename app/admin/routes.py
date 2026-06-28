from flask import render_template
from flask_login import login_required, current_user

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
        return "Unauthorized", 403

    total_users = User.query.count()

    total_treks = Trek.query.count()

    total_staff = User.query.filter_by(
        role="STAFF"
    ).count()

    pending_staff = User.query.filter_by(
        role="STAFF",
        status="PENDING"
    ).count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",

        total_users=total_users,
        total_treks=total_treks,
        total_staff=total_staff,
        pending_staff=pending_staff,
        total_bookings=total_bookings
    )

@admin_bp.route("/treks/create")
@login_required
def create_trek():
    return "<h2>Create Trek Page - Coming Soon</h2>"


@admin_bp.route("/staff")
@login_required
def staff_requests():
    return "<h2>Staff Approval Page - Coming Soon</h2>"


@admin_bp.route("/reports")
@login_required
def reports():
    return "<h2>Reports Page - Coming Soon</h2>"