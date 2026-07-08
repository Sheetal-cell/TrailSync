from flask import jsonify, request
from datetime import datetime

from app.extensions import db
from app.api import api_bp
from app.models import Trek, User, Booking


@api_bp.route("/")
def api_home():

    return jsonify({

        "project":"Trekking Management System API",

        "version":"1.0",

        "available_endpoints":[

            "/api/treks",
            "/api/treks/<id>",
            "/api/users",
            "/api/bookings"

        ]
    })


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


@api_bp.route("/treks", methods=["POST"])
def create_trek():

    data = request.get_json()

    trek = Trek(
        trek_name=data["trek_name"],
        location=data["location"],
        difficulty=data["difficulty"],
        duration=data["duration"],
        available_slots=data["available_slots"],
        start_date=datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ).date(),
        end_date=datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ).date(),
        description=data.get(
            "description",
            ""
        ),
        status=data.get(
            "status",
            "PENDING"
        )
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created successfully.",
        "trek_id": trek.id
    }), 201


@api_bp.route("/treks/<int:trek_id>", methods=["PUT"])
def update_trek_api(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    data = request.get_json()

    trek.trek_name = data.get(
        "trek_name",
        trek.trek_name
    )

    trek.location = data.get(
        "location",
        trek.location
    )

    trek.difficulty = data.get(
        "difficulty",
        trek.difficulty
    )

    trek.duration = data.get(
        "duration",
        trek.duration
    )

    trek.available_slots = data.get(
        "available_slots",
        trek.available_slots
    )

    trek.status = data.get(
        "status",
        trek.status
    )

    db.session.commit()

    return jsonify({
        "message":"Trek updated successfully."
    })

@api_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)

    db.session.commit()

    return jsonify({
        "message":"Trek deleted successfully."
    })

