from flask import Blueprint

staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff"
)

from app.staff import routes
