from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    DateField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange
)
from flask_wtf.file import (
    FileField,
    MultipleFileField,
    FileAllowed
)


class TrekForm(FlaskForm):

    trek_name = StringField(
        "Trek Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    location = StringField(
        "Location",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("Easy", "Easy"),
            ("Moderate", "Moderate"),
            ("Hard", "Hard")
        ],
        validators=[DataRequired()]
    )

    duration = IntegerField(
        "Duration (Days)",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=30)
        ]
    )

    available_slots = IntegerField(
        "Available Slots",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=500)
        ]
    )

    start_date = DateField(
        "Start Date",
        validators=[DataRequired()]
    )

    end_date = DateField(
        "End Date",
        validators=[DataRequired()]
    )

    image = FileField(
        "Cover Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    gallery = MultipleFileField(
        "Gallery Images",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    assigned_staff = SelectField(
        "Assign Staff",
        coerce=int,
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(),
            Length(min=20, max=1000)
        ]
    )

    submit = SubmitField(
        "Create Trek"
    )