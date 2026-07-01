from flask import Blueprint

trekker_bp = Blueprint(
    "trekker",
    __name__
)

from app.trekker import routes