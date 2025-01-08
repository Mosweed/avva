from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from app import app
import mysql.connector
from mysql.connector import Error
from datetime import date




def create_connection():
        try:
            connection = mysql.connector.connect(
                host=app.config["MYSQL_HOST"],
                port=app.config["MYSQL_PORT"],
                user=app.config["MYSQL_USER"],
                password=app.config["MYSQL_PASSWORD"],
                database=app.config["MYSQL_DB"],
            )
            if connection.is_connected():
                print("Connected to MySQL database")
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None


class CheckoutForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d' , validators=[DataRequired()], description="Delivery date" ,
                      render_kw={"min": date.today().strftime('%Y-%m-%d')}
                     )
    delivery_time = SelectField(
        'Delivery Time',
        choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon')],
        validators=[DataRequired()],
        description="Select delivery time"
    )
    tracking_code = StringField(
        'Tracking Code',
        validators=[DataRequired(), Length(max=45)],
        description="Enter tracking code"
    )
    urgent = BooleanField('Urgent', description="Mark if the delivery is urgent")
    delivery_postal_code = StringField(
        'Delivery Postal Code',
        validators=[
            DataRequired(),
            Length(min=6, max=6, message="Postal code must be 6 characters long")
        ],
        description="Enter delivery postal code"
    )
    delivery_house_number = StringField(
        'Delivery House Number',
        validators=[DataRequired(), Length(max=6)],
        description="Enter delivery house number"
    )
    delivery_city = StringField(
        'Delivery City',
        validators=[DataRequired(), Length(max=45)],
        description="Enter delivery city"
    )
    submit = SubmitField('Submit')