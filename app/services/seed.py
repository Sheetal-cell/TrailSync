from app.models import User
from app.extensions import db
from app.utils.security import hash_password

def create_admin():

    admin = User.query.filter_by(
        email="admin@trailsync.com"
    ).first()

    if admin:
        return

    admin = User(
        full_name="System Administrator",
        email="admin@trailsync.com",
        password=hash_password("admin123"),
        phone="9999999999",
        role="ADMIN",
        status="APPROVED",
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Default Admin Created")