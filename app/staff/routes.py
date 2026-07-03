from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.extensions import db
from flask_login import login_required, current_user
from app.staff import staff_bp
from app.models import (
    Trek,
    Booking,
    User
)

@staff_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "STAFF":
        return "Unauthorized", 403

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=current_user.id
    ).all()

    total_treks = len(assigned_treks)

    open_treks = sum(
        1 for trek in assigned_treks
        if trek.status == "OPEN"
    )

    completed_treks = sum(
        1 for trek in assigned_treks
        if trek.status == "COMPLETED"
    )

    total_trekkers = sum(
        len(trek.bookings)
        for trek in assigned_treks
    )

    return render_template(
        "staff/dashboard.html",
        assigned_treks=assigned_treks,
        total_treks=total_treks,
        open_treks=open_treks,
        completed_treks=completed_treks,
        total_trekkers=total_trekkers
    )

@staff_bp.route("/trek/<int:trek_id>")
@login_required
def trek_details(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != current_user.id:
        return "Unauthorized", 403

    return render_template(
        "staff/trek_details.html",
        trek=trek
    )

@staff_bp.route("/trek/<int:trek_id>/slots", methods=["GET","POST"])
@login_required
def edit_slots(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != current_user.id:
        return "Unauthorized",403

    if request.method == "POST":

        trek.available_slots = int(
            request.form["slots"]
        )

        db.session.commit()

        flash(
            "Slots updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "staff.trek_details",
                trek_id=trek.id
            )
        )

    return render_template(
        "staff/edit_slots.html",
        trek=trek
    )

@staff_bp.route("/trek/<int:trek_id>/status", methods=["GET","POST"])
@login_required
def update_status(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != current_user.id:
        return "Unauthorized",403

    if request.method=="POST":

        trek.status = request.form["status"]

        db.session.commit()

        flash(
            "Status updated.",
            "success"
        )

        return redirect(
            url_for(
                "staff.trek_details",
                trek_id=trek.id
            )
        )

    return render_template(
        "staff/update_status.html",
        trek=trek
    )

@staff_bp.route("/trek/<int:trek_id>/participants")
@login_required
def participants(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != current_user.id:
        return "Unauthorized",403

    return render_template(
        "staff/participants.html",
        trek=trek
    )

