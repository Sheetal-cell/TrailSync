from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from flask_login import login_required, current_user

from app.trekker import trekker_bp
from app.models import (
    Trek,
    Booking
)
from app.extensions import db
from app.auth.forms import ProfileForm

@trekker_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")

    query = Trek.query.filter(
        Trek.status == "OPEN",
        Trek.available_slots > 0
    )

    if difficulty:
        query = query.filter(
            Trek.difficulty == difficulty
        )

    if location:
        query = query.filter(
            Trek.location.ilike(f"%{location}%")
        )

    treks = query.all()

    booking_count = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "trekker/dashboard.html",
        treks=treks,
        difficulty=difficulty,
        location=location,
        booking_count=booking_count
    )


@trekker_bp.route("/trek/<int:trek_id>")
@login_required
def trek_details(trek_id):

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    return render_template(
        "trekker/trek_details.html",
        trek=trek
    )

@trekker_bp.route("/book/<int:trek_id>")
@login_required
def book_trek(trek_id):

    print("BOOK ROUTE HIT")

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "OPEN":

        flash(
            "This trek is not open for booking.",
            "danger"
        )

        return redirect(
            url_for(
                "trekker.trek_details",
                trek_id=trek.id
            )
        )

    print("Booking trek:", trek.id)

    existing_booking = Booking.query.filter(
        Booking.user_id == current_user.id,
        Booking.trek_id == trek.id,
        Booking.booking_status != "CANCELLED"
    ).first()

    if existing_booking:
        print("Already booked")
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("trekker.trek_details", trek_id=trek.id))

    print("Creating booking")

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_status="BOOKED",
        payment_status="PENDING"
    )

    db.session.add(booking)

    trek.available_slots -= 1

    db.session.commit()

    print("Booking saved successfully")

    flash("Trek booked successfully!", "success")

    flash(
        "Trek booked successfully!",
        "success"
    )



    return redirect(url_for("trekker.my_bookings"))

@trekker_bp.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "trekker/my_bookings.html",
        bookings=bookings
    )


@trekker_bp.route("/booking/<int:booking_id>/cancel")
@login_required
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        return "Unauthorized", 403

    # Don't allow cancellation after trek has started
    if booking.trek.status in ["ONGOING", "COMPLETED"]:

        flash(
            "This booking can no longer be cancelled.",
            "danger"
        )

        return redirect(
            url_for("trekker.my_bookings")
        )

    booking.booking_status = "CANCELLED"

    booking.trek.available_slots += booking.number_of_people

    db.session.commit()

    flash(
        "Booking cancelled successfully.",
        "success"
    )

    return redirect(
        url_for("trekker.my_bookings")
    )

@trekker_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("trekker.profile")
        )

    return render_template(
        "trekker/profile.html",
        form=form
    )

@trekker_bp.route("/history")
@login_required
def history():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "trekker/history.html",
        bookings=bookings
    )

