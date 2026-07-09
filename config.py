import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "trailsync-secret-key"
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'trailsync.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    QR_FOLDER = os.path.join(BASE_DIR, "app", "static", "qr")
    UPLOAD_FOLDER = os.path.join(
    "app",
    "static",
    "uploads"
    )

SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

REMEMBER_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_SECURE = False