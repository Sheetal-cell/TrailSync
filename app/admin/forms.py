from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    DateField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired


class TrekForm(FlaskForm):

    trek_name = StringField(
        "Trek Name",
        validators=[DataRequired()]
    )

    location = StringField(
        "Location",
        validators=[DataRequired()]
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("Easy", "Easy"),
            ("Moderate", "Moderate"),
            ("Hard", "Hard")
        ]
    )

    duration = IntegerField(
        "Duration (Days)",
        validators=[DataRequired()]
    )

    available_slots = IntegerField(
        "Available Slots",
        validators=[DataRequired()]
    )

    start_date = DateField(
        "Start Date",
        validators=[DataRequired()]
    )

    end_date = DateField(
        "End Date",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    submit = SubmitField(
        "Create Trek"
    )