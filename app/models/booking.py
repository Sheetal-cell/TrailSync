from datetime import datetime
from app.extensions import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )
    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    booking_status = db.Column(
        db.String(20),
        nullable=False,
        default="BOOKED"
    )
    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    attendance_status = db.Column(
        db.String(20),
        default="REGISTERED"
    )
    number_of_people = db.Column(
        db.Integer,
        default=1
    )
    total_amount = db.Column(
        db.Float,
        default=0.0
    )

    user = db.relationship(
        "User",
        back_populates="bookings"
    )

    trek = db.relationship(
        "Trek",
        back_populates="bookings"
    )


    def __repr__(self):
        return f"<Booking #{self.id}>"