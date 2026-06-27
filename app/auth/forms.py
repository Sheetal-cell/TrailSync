from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)

class RegistrationForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=10, max=15)
        ]
    )
    role = SelectField(
        "Register As",
        choices=[
            ("TREKKER", "Trekker"),
            ("STAFF", "Trek Staff")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")