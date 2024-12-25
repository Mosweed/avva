
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField, SelectField, SelectMultipleField , widgets 
from wtforms.validators import DataRequired, Optional, NumberRange , ValidationError
from App.classes.suppliers import Supplier
from App.classes.products import Product


ADVICE_OPTIONS = Product.get_advice_options()
STORAGE_LOCATIONS = Product.get_storage_locations()
SUPPLIERS = Supplier.get_id_and_name()


class ProductForm(FlaskForm):
    
    productID = StringField('Product ID',  render_kw={'readonly': True})
    name = StringField('Name', validators=[DataRequired()])
    article_number = StringField('Article Number',render_kw={'readonly': True})
    stock = IntegerField('Stock', validators=[NumberRange(min=0), DataRequired()])
    minimum_stock = IntegerField('Minimum Stock', validators=[DataRequired(), NumberRange(min=0)])
    perishable = BooleanField('Perishable')
    adviceID = SelectField('Advice', choices=ADVICE_OPTIONS, validators=[DataRequired()])
    energy_cost = FloatField('Energy Cost', validators=[DataRequired(), NumberRange(min=0)])
    packaging_size = StringField('Packaging Size', validators=[DataRequired()])
    storage_locationID = SelectField('Storage Location', choices=STORAGE_LOCATIONS, validators=[DataRequired()])
    suppliers = SelectMultipleField('Suppliers', choices=SUPPLIERS, validators=[Optional()], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Submit')