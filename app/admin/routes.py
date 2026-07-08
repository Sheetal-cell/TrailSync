from flask import (
    render_template,
    redirect,
    url_for,
    request,
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

    total_bookings = Booking.query.count()

    active_bookings = Booking.query.filter_by(
        booking_status="BOOKED"
    ).count()

    cancelled_bookings = Booking.query.filter_by(
        booking_status="CANCELLED"
    ).count()

    completed_bookings = Booking.query.filter_by(
        booking_status="COMPLETED"
    ).count()

    pending_payment = Booking.query.filter_by(
        payment_status="PENDING"
    ).count()

    paid_payment = Booking.query.filter_by(
        payment_status="PAID"
    ).count()

    recent_bookings = Booking.query.order_by(
        Booking.booking_date.desc()
    ).limit(5).all()

    recent_users = User.query.order_by(
        User.created_at.desc()
    ).limit(3).all()

    chart_labels = [
        "Treks",
        "Bookings",
        "Trekkers",
        "Staff"
    ]

    chart_values = [
        total_treks,
        total_bookings,
        total_trekkers,
        total_staff
    ]

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        pending_staff=pending_staff,
        total_trekkers=total_trekkers,
        total_treks=total_treks,
        total_bookings=total_bookings,
        active_bookings=active_bookings,
        cancelled_bookings=cancelled_bookings,
        recent_bookings=recent_bookings,
        recent_users=recent_users,
        completed_bookings=completed_bookings,
        pending_payment=pending_payment,
        paid_payment=paid_payment,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

@admin_bp.route("/treks/create", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    form = TrekForm()
    staff = User.query.filter_by(
        role="STAFF",
        status="APPROVED"
    ).all()

    form.assigned_staff.choices = [
        (0, "No Staff")
    ]

    form.assigned_staff.choices += [
        (s.id, s.full_name)
        for s in staff
    ]

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
            assigned_staff_id=(
                form.assigned_staff.data
                if form.assigned_staff.data != 0
                else None
            ),

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

    search = request.args.get("search", "")
    treks = Trek.query
    if search:
        treks = treks.filter(
            Trek.trek_name.ilike(f"%{search}%")
        )

    treks = treks.order_by(
        Trek.start_date.desc()
    ).all()

    return render_template(
        "admin/all_treks.html",
        treks=treks,
        search=search
    )
@admin_bp.route("/bookings")
@login_required
def bookings():

    
    print(request.args)
    search = request.args.get("search", "")
    booking_status = request.args.get("booking_status", "")
    payment_status = request.args.get("payment_status", "")

    print(search)
    print(booking_status)
    print(payment_status)

    query = Booking.query

    if search:
        query = query.join(User).filter(
            User.full_name.ilike(f"%{search}%")
        )
    if booking_status:
        query = query.filter(
            Booking.booking_status == booking_status
        )
    if payment_status:
        query = query.filter(
            Booking.payment_status == payment_status
        )
    bookings = query.order_by(
        Booking.booking_date.desc()
    ).all()
    return render_template(
        "admin/bookings.html",
        bookings=bookings,
        search=search,
        booking_status=booking_status,
        payment_status=payment_status
    )

@admin_bp.route("/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    form = TrekForm(obj=trek)
    staff = User.query.filter_by(
        role="STAFF",
        status="APPROVED"
    ).all()

    form.assigned_staff.choices = [
        (0, "No Staff")
    ]

    form.assigned_staff.choices += [
        (s.id, s.full_name)
        for s in staff
    ]

    if request.method == "GET":
        form.assigned_staff.data = (
            trek.assigned_staff_id or 0
        )

    if form.validate_on_submit():

        trek.trek_name = form.trek_name.data
        trek.location = form.location.data
        trek.difficulty = form.difficulty.data
        trek.duration = form.duration.data
        trek.available_slots = form.available_slots.data
        trek.start_date = form.start_date.data
        trek.end_date = form.end_date.data
        trek.description = form.description.data

        trek.assigned_staff_id = (
            form.assigned_staff.data
            if form.assigned_staff.data != 0
            else None
        )

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

    search = request.args.get("search", "")

    query = User.query.filter_by(role="STAFF")

    if search:
        query = query.filter(
            User.full_name.ilike(f"%{search}%")
        )

    pending_staff = User.query.filter_by(
        role="STAFF",
        status="PENDING"
        ).all()

    approved_staff = User.query.filter_by(
        role="STAFF",
        status="APPROVED",
        is_active=True
    ).all()

    return render_template(
        "admin/staff.html",
        staff_members=pending_staff,
        approved_staff=approved_staff
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
    search = request.args.get("search", "")
    users = User.query.filter(User.role=="TREKKER")
    if search:
        users = users.filter(
            User.full_name.ilike(f"%{search}%")
        )
    users = users.order_by(
        User.created_at.desc()
    ).all()
    return render_template(
        "admin/users.html",
        users=users,
        search=search
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


@admin_bp.route("/users/toggle/<int:user_id>")
@login_required
def toggle_user(user_id):

    if current_user.role != "ADMIN":
        return "Unauthorized", 403

    user = User.query.get_or_404(user_id)

    # Prevent deactivating yourself
    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "danger")
        return redirect(url_for("admin.users"))

    # Prevent deactivating any admin account
    if user.role == "ADMIN":
        flash("Admin accounts cannot be deactivated.", "danger")
        return redirect(url_for("admin.users"))

    user.is_active = not user.is_active

    if user.is_active:
        flash("User activated.", "success")
    else:
        flash("User deactivated.", "warning")

    db.session.commit()

    return redirect(url_for("admin.users"))


@admin_bp.route("/history")
@login_required
def trek_history():

    bookings = Booking.query.order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "admin/history.html",
        bookings=bookings
    )