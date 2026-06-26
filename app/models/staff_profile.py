from datetime import datetime
from app.extensions import db


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    bio = db.Column(db.Text)
    experience = db.Column(
        db.Integer,
        default=0
    )
    emergency_contact = db.Column(
        db.String(15)
    )
    certifications = db.Column(
        db.Text
    )
    specialization = db.Column(
        db.String(100)
    )
    profile_image = db.Column(
        db.String(255),
        default="default_profile.png"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    user = db.relationship(
        "User",
        back_populates="staff_profile"
    )
    def __repr__(self):
        return f"<StaffProfile {self.user_id}>"