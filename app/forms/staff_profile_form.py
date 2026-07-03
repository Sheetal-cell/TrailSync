from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import DataRequired

class StaffProfileForm(FlaskForm):

    phone = StringField(
        "Phone",
        validators=[DataRequired()]
    )

    bio = TextAreaField(
        "Bio"
    )

    submit = SubmitField(
        "Update Profile"
    )