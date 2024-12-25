
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField, SelectField, SelectMultipleField , widgets 
from wtforms.validators import DataRequired, Optional, NumberRange , ValidationError
from App.classes.suppliers import Supplier


ADVICE_OPTIONS = [("1", "Advice 1"), ("2", "Advice 2"), ("3", "Advice 3")]
STORAGE_LOCATIONS = [("1", "Location A"), ("2", "Location B"), ("3", "Location C")]
SUPPLIERS = Supplier.get_id_and_name()



def validate_unique_article_number(form, field):
    # Simulate a database call to check uniqueness
    existing_article_numbers = ["12345", "67890"]  # Dit zou uit de database moeten komen
    if field.data in existing_article_numbers:
        raise ValidationError('Article Number must be unique.')

class ProductForm(FlaskForm):
    
    productID = StringField('Product ID', validators=[DataRequired() ], render_kw={'readonly': True})
    name = StringField('Name', validators=[DataRequired()])
    article_number = StringField('Article Number', validators=[ validate_unique_article_number , DataRequired()] )
    stock = IntegerField('Stock', validators=[NumberRange(min=0), DataRequired()])
    minimum_stock = IntegerField('Minimum Stock', validators=[DataRequired(), NumberRange(min=0)])
    perishable = BooleanField('Perishable')
    adviceID = SelectField('Advice', choices=ADVICE_OPTIONS, validators=[DataRequired()])
    energy_cost = FloatField('Energy Cost', validators=[DataRequired(), NumberRange(min=0)])
    packaging_size = StringField('Packaging Size', validators=[DataRequired()])
    storage_locationID = SelectField('Storage Location', choices=STORAGE_LOCATIONS, validators=[DataRequired()])
    suppliers = SelectMultipleField('Suppliers', choices=SUPPLIERS, validators=[Optional()], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Submit')