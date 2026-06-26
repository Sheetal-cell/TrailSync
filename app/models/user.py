from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(
        db.String(20),
        nullable=False,
        default="TREKKER"
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )
    is_active = db.Column(
        db.Boolean,
        default=True
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    def __repr__(self):
        return f"<User {self.full_name}>"