from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    BooleanField,
    SubmitField,
    SelectField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import (
    DataRequired,
    Optional,
    NumberRange,
    ValidationError,
    InputRequired
)
from App.classes.suppliers import Supplier
from App.classes.products import Product


ADVICE_OPTIONS = Product.get_advice_options()
STORAGE_LOCATIONS = Product.get_storage_locations()
SUPPLIERS = Supplier.get_id_and_name()


class ProductForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    article_number = StringField("Article Number", render_kw={"readonly": True})
    stock = IntegerField("Stock", validators=[NumberRange(min=0), DataRequired()])
    minimum_stock = IntegerField("Minimum Stock", validators=[DataRequired(), NumberRange(min=0)])
    perishable = BooleanField("Perishable")
    adviceID = SelectField("Advice", choices=ADVICE_OPTIONS, validators=[DataRequired()])
    energy_cost = StringField("Energy Cost", validators=[DataRequired()])
    packaging_size = StringField("Packaging Size", validators=[DataRequired()])
    price = FloatField(
        'Price',
        validators=[
            InputRequired(message="This field is required."),
            NumberRange(min=0.0, message="Value must be moor than 0 .")
        ]
    )
    storage_locationID = SelectField(
        "Storage Location",
        choices=STORAGE_LOCATIONS,
        validators=[DataRequired()],
    )
    suppliers = SelectMultipleField(
        "Suppliers",
        choices=SUPPLIERS,
        validators=[Optional()],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
    )
    submit = SubmitField("Submit")


class EditProductForm(FlaskForm):
    # Read-only fields to prevent editing
    productID = StringField("Product ID", render_kw={"readonly": True})
    article_number = StringField("Article Number", render_kw={"readonly": True})

    # Editable fields
    name = StringField("Name", validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[NumberRange(min=0), DataRequired()])
    minimum_stock = IntegerField("Minimum Stock", validators=[DataRequired(), NumberRange(min=0)])
    perishable = BooleanField("Perishable")
    adviceID = SelectField("Advice", choices=ADVICE_OPTIONS, validators=[DataRequired()])
    energy_cost = StringField("Energy Cost", validators=[DataRequired()])
    packaging_size = StringField("Packaging Size", validators=[DataRequired()])
    price = FloatField(
        'Price',
        validators=[
            InputRequired(message="This field is required."),
            NumberRange(min=0.0, message="Value must be moor than 0 .")
        ]
    )
    storage_locationID = SelectField(
        "Storage Location",
        choices=STORAGE_LOCATIONS,
        validators=[DataRequired()],
    )
    suppliers = SelectMultipleField(
        "Suppliers",
        choices=SUPPLIERS,
        validators=[Optional()],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
    )

    # Submit button
    submit = SubmitField("Save Changes")
