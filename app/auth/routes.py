from flask import render_template
from app.auth import auth_bp

@auth_bp.route("/login")
def login():

    return render_template(
        "auth/login.html"
    )

@auth_bp.route("/register")
def register():

    return render_template(
        "auth/register.html"
    )