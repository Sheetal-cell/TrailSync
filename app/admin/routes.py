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
import os

from flask import current_app
from werkzeug.utils import secure_filename
from app.models import TrekGallery



@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    total_users = User.query.count()

    total_staff = User.query.filter_by(
        role="STAFF"
    ).count()

    pending_staff = User.query.filter_by(
        role="STAFF",
        status="PENDING"
    ).count()

    total_trekkers = User.query.filter_by(
        role="TREKKER"
    ).count()

    total_treks = Trek.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        pending_staff=pending_staff,
        total_trekkers=total_trekkers,
        total_treks=total_treks
    )

@admin_bp.route("/treks/create", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    form = TrekForm()

    if form.validate_on_submit():

        cover_image = None

        if form.image.data:

            file = form.image.data

            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            cover_image = filename

        trek = Trek(

            trek_name=form.trek_name.data,
            location=form.location.data,
            difficulty=form.difficulty.data,
            duration=form.duration.data,
            available_slots=form.available_slots.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            status="OPEN",

            image=cover_image

        )

        db.session.add(trek)

        db.session.commit()

        if form.gallery.data:

            for file in form.gallery.data:

                if file.filename == "":
                    continue

                filename = secure_filename(
                    file.filename
                )

                file.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )
                
                gallery = TrekGallery(
                    trek_id=trek.id,
                    image=filename
                )

                db.session.add(gallery)
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

@admin_bp.route("/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    form = TrekForm(obj=trek)

    if form.validate_on_submit():

        form.populate_obj(trek)

        db.session.commit()

        flash(
            "Trek updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.all_treks")
        )

    return render_template(
        "admin/create_trek.html",
        form=form
    )

@admin_bp.route("/treks/delete/<int:trek_id>")
@login_required
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)

    db.session.commit()

    flash(
        "Trek deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.all_treks")
    )

@admin_bp.route("/staff")
@login_required
def staff():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    staff_members = User.query.filter_by(role="STAFF").all()

    return render_template(
        "admin/staff.html",
        staff_members=staff_members
    )

@admin_bp.route("/staff/approve/<int:user_id>")
@login_required
def approve_staff(user_id):

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    staff = User.query.get_or_404(user_id)

    staff.status = "APPROVED"

    db.session.commit()

    flash(
        "Staff approved successfully.",
        "success"
    )

    return redirect(
        url_for("admin.staff")
    )


@admin_bp.route("/users")
@login_required
def users():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    users = User.query.order_by(User.created_at.desc()).all()

    return render_template(
        "admin/users.html",
        users=users
    )

@admin_bp.route("/treks/<int:trek_id>")
@login_required
def trek_details(trek_id):

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    return render_template(
        "admin/trek_details.html",
        trek=trek
    )