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

@trekker_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    location = request.args.get("location", "")
    difficulty = request.args.get("difficulty", "")

    treks = Trek.query.filter_by(status="OPEN")

    if location:
        treks = treks.filter(
            Trek.location.ilike(f"%{location}%")
        )

    if difficulty:
        treks = treks.filter_by(
            difficulty=difficulty
        )

    treks = treks.all()

    return render_template(
        "trekker/dashboard.html",
        treks=treks,
        location=location,
        difficulty=difficulty
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

    print("Booking trek:", trek.id)

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_status="BOOKED"
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

@trekker_bp.route("/cancel-booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        return "Unauthorized", 403

    if booking.booking_status == "CANCELLED":

        flash(
            "Booking already cancelled.",
            "warning"
        )

        return redirect(
            url_for("trekker.my_bookings")
        )

    booking.booking_status = "CANCELLED"
    booking.trek.available_slots += 1

    db.session.commit()

    flash(
        "Booking cancelled successfully.",
        "success"
    )

    return redirect(
        url_for("trekker.my_bookings")
    )