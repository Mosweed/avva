from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField ,EmailField
from wtforms.validators import DataRequired, Length, Email, NumberRange 

class CustomerForm(FlaskForm):
    name = StringField(
        "Customer Name",
        validators=[DataRequired(), Length(min=2, max=255)],
        render_kw={"placeholder": "Enter customer name"}
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Length(min=7, max=20)],
        render_kw={"placeholder": "Enter phone number"}
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(),],
        render_kw={"placeholder": "Enter email address"}
    )
    street_name = StringField(
        "Street Name",
        validators=[DataRequired(), Length(max=255)],
        render_kw={"placeholder": "Enter street name"}
    )
    house_number = StringField(
        "House Number",
        validators=[DataRequired(), Length(max=10)],
        render_kw={"placeholder": "Enter house number"}
    )
    postal_code = StringField(
        "Postal Code",
        validators=[DataRequired(), Length(max=6)],
        render_kw={"placeholder": "Enter postal code"}
    )
    city = StringField(
        "City",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"placeholder": "Enter city"}
    )
    submit = SubmitField("Save")
