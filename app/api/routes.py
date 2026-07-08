from flask import jsonify

from app.api import api_bp
from app.models import Trek
from app.models import User
from app.models import Booking

@api_bp.route("/treks")
def get_treks():

    treks = Trek.query.all()

    data = []

    for trek in treks:

        data.append({

            "id": trek.id,

            "trek_name": trek.trek_name,

            "location": trek.location,

            "difficulty": trek.difficulty,

            "duration": trek.duration,

            "available_slots": trek.available_slots,

            "status": trek.status,

            "start_date": str(trek.start_date),

            "end_date": str(trek.end_date)

        })

    return jsonify(data)

@api_bp.route("/treks/<int:trek_id>")
def get_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    return jsonify({

        "id": trek.id,

        "trek_name": trek.trek_name,

        "location": trek.location,

        "difficulty": trek.difficulty,

        "description": trek.description,

        "duration": trek.duration,

        "available_slots": trek.available_slots,

        "status": trek.status,

        "start_date": str(trek.start_date),

        "end_date": str(trek.end_date)

    })

@api_bp.route("/users")
def get_users():

    users = User.query.all()

    result = []

    for user in users:

        result.append({

            "id": user.id,

            "name": user.full_name,

            "email": user.email,

            "role": user.role,

            "status": user.status

        })

    return jsonify(result)

@api_bp.route("/bookings")
def get_bookings():

    bookings = Booking.query.all()

    result = []

    for booking in bookings:

        result.append({

            "id": booking.id,

            "trekker": booking.user.full_name,

            "trek": booking.trek.trek_name,

            "booking_status": booking.booking_status,

            "payment_status": booking.payment_status,

            "attendance_status": booking.attendance_status,

            "booking_date": str(booking.booking_date)

        })

    return jsonify(result)