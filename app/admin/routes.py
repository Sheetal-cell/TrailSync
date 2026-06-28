from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import login_required, current_user
from app.admin.forms import TrekForm
from app.extensions import db

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

@admin_bp.route("/treks/create", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    form = TrekForm()

    if form.validate_on_submit():

        trek = Trek(
            trek_name=form.trek_name.data,
            location=form.location.data,
            difficulty=form.difficulty.data,
            duration=form.duration.data,
            available_slots=form.available_slots.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            status="OPEN"
        )

        db.session.add(trek)
        db.session.commit()

        flash(
            "Trek created successfully!",
            "success"
        )

        return redirect(
            url_for("admin.all_treks")
        )

    return render_template(
        "admin/create_trek.html",
        form=form
    )

@admin_bp.route("/staff")
@login_required
def staff_requests():
    return "<h2>Staff Approval Page - Coming Soon</h2>"


@admin_bp.route("/reports")
@login_required
def reports():
    return "<h2>Reports Page - Coming Soon</h2>"

@admin_bp.route("/treks")
@login_required
def all_treks():

    treks = Trek.query.order_by(
        Trek.start_date
    ).all()

    return render_template(
        "admin/all_treks.html",
        treks=treks
    )