from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class PaymentForm(FlaskForm):

    booking_id = HiddenField()

    submit = SubmitField("Pay Now")