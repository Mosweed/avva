from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField ,EmailField , ValidationError
from wtforms.validators import DataRequired, Length, Email, NumberRange 
from app import app
import mysql.connector
from mysql.connector import Error
from App.classes.customers import Customer



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

def validate_email_if_exist(form, field):
    email = field.data
    if "@" not in email:
        raise ValidationError("Email must contain '@'.")
    if "." not in email:
        raise ValidationError("Email must contain a '.'.")

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM customers WHERE email = %s"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                raise ValidationError("This email already exists in the system.")
        except Error as e:
            print(f"Error during customer retrieval: {e}")
        finally:
            cursor.close()
            connection.close()

# CustomerForm definition
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
        validators=[DataRequired(), validate_email_if_exist],
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
    
    
    
    
def validate_email_if_exist_for_edit(form, field):
    email = field.data
    customer_id = form.customer_id.data

    print("customer_id",customer_id)
    if "@" not in email:
        raise ValidationError("Email must contain '@'.")
    if "." not in email:
        raise ValidationError("Email must contain a '.'.")

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM customers WHERE email = %s AND id != %s"
            cursor.execute(query, (email, customer_id))
            row = cursor.fetchone()
            if row:
                raise ValidationError("This email is already registered with another customer.")
        except Error as e:
            print(f"Error during customer retrieval: {e}")
        finally:
            cursor.close()
            connection.close()

# EditCustomerForm definition
class EditCustomerForm(FlaskForm):
    customer_id = IntegerField("Customer ID", render_kw={"readonly": True}  )
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
        validators=[DataRequired(), validate_email_if_exist_for_edit],
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
    submit = SubmitField("Save Changes")