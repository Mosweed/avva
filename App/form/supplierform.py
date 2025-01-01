from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class SupplierForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=255)],
        render_kw={"placeholder": "Enter supplier name"}
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Length(min=7, max=20)],
        render_kw={"placeholder": "Enter phone number"}
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
    website = StringField(
        "Website",
        validators=[Optional()],
        render_kw={"placeholder": "Enter website URL (optional)"}
    )
    submit = SubmitField("Submit")


class EditSupplierForm(FlaskForm):
    supplierID = StringField(
        "Supplier ID", render_kw={"readonly": True}
    )
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=255)],
        render_kw={"placeholder": "Enter supplier name"}
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Length(min=7, max=20)],
        render_kw={"placeholder": "Enter phone number"}
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
    website = StringField(
        "Website",
        validators=[Optional()],
        render_kw={"placeholder": "Enter website URL (optional)"}
    )
    submit = SubmitField("Save Changes")
