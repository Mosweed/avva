from flask import (
    Flask,
    redirect,
    url_for,
    request,
    render_template,
    jsonify,
    flash,
    abort
)

import time
from app import app, mail
import mysql.connector
from mysql.connector import Error
from App.classes.products import Product
from App.classes.suppliers import Supplier
from App.classes.customers import Customer
from App.classes.orders import Order
from flask_mail import Message
from flask import session
import random
import string
from App.form.supplierform import SupplierForm ,EditSupplierForm
from App.form.customerform import CustomerForm ,EditCustomerForm
from App.form.productform import ProductForm, EditProductForm
from App.form.checkoutform import CheckoutForm

from logging_config import logger


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
            return connection
    except Error as e:
        logger.error(f" A critical error has occurred in  create_connection(): {e} ")
        
        return None


def calculate_co2_truck(distance_km, emission_per_km=900):
    total_grams = distance_km * emission_per_km
    total_kg = total_grams / 1000  # Convert to kilograms
    return total_kg


@app.route("/Dashboard")
@app.route("/")
def dashboard():

    standard_co2 = calculate_co2_truck(random.randint(100, 500))
    express_co2 = calculate_co2_truck(random.randint(100, 500) + 200)

    connection = create_connection()
    if not connection:
        return render_template(
            "dashboard.html",
            products=[],
            standard_co2=standard_co2,
            express_co2=express_co2,
        )
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT p.productID , p.name , p.stock , p.minimum_stock   FROM products p  where stock  <= minimum_stock "
        )  
        rows = cursor.fetchall()

        products = [
            Product(
                row["productID"],
                row["name"],
                row["stock"],
                row["minimum_stock"],
            )
            for row in rows
        ]
        return render_template(
            "dashboard.html",
            products=products,
            standard_co2=standard_co2,
            express_co2=express_co2,
        )
    # return jsonify([t.__dict__ for t in products])

    except Error as e:
        abort(500)
        logger.error(f" A critical error has occurred in  dashboard(): {e} ")        
        
    finally:
        cursor.close()
        connection.close()


@app.route("/products")
def products():

    try:

        return render_template("products/products.html")

    except Error as e:
       abort(500)
       logger.error(f" A critical error has occurred in  products(): {e} ")
    finally:
        print("Done")


@app.route("/products/<product_id>")
def product(product_id):
    
    try:
        product = Product.get_by_id(product_id)

        if not product:
            abort( 404)
        suppliers = product.get_suppliers()
        price_history = product.get_price_history()
        
        return render_template("products/product_view.html", product=product, suppliers=suppliers , price_history=price_history)
    except Error as e:
        abort(500)
        logger.error(f" A critical error has occurred in  product(): {e} ")
    finally:
        print("Done")

# Functie om een artikelnummer te controleren en toe te voegen
def create_unique_article():
    while True:
        # Genereer een nieuw artikelnummer
        article_number = "".join(random.choices(string.digits, k=6))
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Controleer of het al in de database staat
        query = "SELECT * FROM s2232599.products where article_number  = %s"
        cursor.execute(query, (article_number,))
        exists = cursor.fetchone()

        if not exists:
            return article_number


@app.route("/products/create", methods=["GET", "POST"])
def product_create():

    article_number = create_unique_article()
    data = {
        "article_number": article_number,
    }
    form = ProductForm(data=data)

    print(form.article_number.data)
    if form.validate_on_submit():

        product = Product(
            name=form.name.data,
            article_number=form.article_number.data,
            stock=form.stock.data,
            minimum_stock=form.minimum_stock.data,
            perishable=form.perishable.data,
            adviceID=form.adviceID.data,
            energy_cost=form.energy_cost.data,
            packaging_size=form.packaging_size.data,
            storage_locationID=form.storage_locationID.data,
            price=form.price.data,
        )

        suppliers = form.suppliers.data

        try:
            product.create()

            for supplier_id in suppliers:
                product.add_supplier(supplier_id)

            flash(
                f"Product {product.name} aangemaakt met ID {product.productID}",
                "success",
            )
            return redirect(url_for("products"))
        except Error as e:
           abort(500)
           logger.error(f" A critical error has occurred in  product_create(): {e} ")

    return render_template("products/product_create_form.html", form=form)


@app.route("/products/edit/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
   

    prise = product.price
    # Vul product_data met gegevens uit de database
    product_data = {
        "productID": product.productID,
        "name": product.name,
        "article_number": product.article_number,
        "stock": product.stock,
        "minimum_stock": product.minimum_stock,
        "perishable": product.perishable,
        "adviceID": product.adviceID,
        "energy_cost": product.energy_cost,
        "packaging_size": product.packaging_size,
        "storage_locationID": product.storage_locationID,
        "suppliers": [supplier.supplierID for supplier in product.get_suppliers()],
        "price": product.price,
    }

    # Maak een formulier gebaseerd op deze data
    form = EditProductForm(data=product_data)

    if form.validate_on_submit():
        try:
            # Update product-object met nieuwe data
            
            print(form.name.data)
            
            product.name = form.name.data
            product.stock = form.stock.data
            product.minimum_stock = form.minimum_stock.data
            product.perishable = form.perishable.data
            product.adviceID = form.adviceID.data
            product.energy_cost = form.energy_cost.data
            product.packaging_size = form.packaging_size.data
            product.storage_locationID = form.storage_locationID.data
            product.price = form.price.data

            product.edit()
            
            if prise != form.price.data:
                product.update_price_history(prise)

            # Werk de leveranciers bij als dat nodig is
            if form.suppliers.data:
                product.clear_suppliers()
                for supplier_id in form.suppliers.data:
                    product.add_supplier(supplier_id)

            flash(f"Product '{product.name}' is succesvol bijgewerkt.", "success")
            return redirect(url_for("products"))
        except Exception as e:
            flash(f"An error has occurred", "danger")
            logger.error(f" A critical error has occurred in  edit_product(): {e} ")


    # Render het formulier als de submit faalt of GET-methode
    return render_template("products/product_edit_form.html", form=form, product_id=product_id)


@app.route("/products_list")
def products_list():
    try:
        return render_template("products/products_list.html")
    except Error as e:
        abort(500)
        logger.error(f" A critical error has occurred in  product_list(): {e} ")
    


@app.route("/suppliers")
def suppliers():

    try:
       
        return render_template("suppliers/suppliers.html")

    except Error as e:
        abort(500)
        logger.error(f" A critical error has occurred in  suppliers(): {e} ")
   
  


@app.route("/suppliers/<int:supplier_id>")
def supplier_view(supplier_id):
    try:
        # Haal de specifieke leverancier op
        supplier = Supplier.get_by_id(supplier_id)
        if not supplier:
            abort(404)

        # Haal producten op die aan de leverancier gekoppeld zijn

        # Render de pagina met supplier details en gekoppelde producten
        return render_template("suppliers/supplier_view.html", supplier=supplier)

    except Error as e:
        abort(500)
        logger.error(f" A critical error has occurred in  supplier_view(): {e} ")
   


@app.route("/suppliers/create", methods=["GET", "POST"])
def supplier_create():
    form = SupplierForm()
    if form.validate_on_submit():
    

        name = form.name.data
        phone_number = form.phone_number.data
        street_name = form.street_name.data
        house_number = form.house_number.data
        postal_code = form.postal_code.data
        website = form.website.data
        
        # Maak een nieuwe leverancier
        new_supplier = Supplier(
            name=name,
            phone_number=phone_number,
            street_name=street_name,
            house_number=house_number,
            postal_code=postal_code,
            website=website,
        )
        try:
            
            new_supplier.create()
            flash("Supplier added successfully!", "success")
            return redirect(url_for("suppliers"))
        except Error as e:
            abort(500)
            logger.error(f" A critical error has occurred in  supplier_create(): {e} ")

    return render_template("suppliers/supplier_create.html" , form=form)


@app.route("/suppliers/edit/<int:supplier_id>", methods=["GET", "POST"])
def supplier_edit(supplier_id):

    supplier = Supplier.get_by_id(supplier_id)
    if not supplier:
        abort(404)
        
    form = EditSupplierForm(
        supplier_id=supplier.supplierID,
        name=supplier.name,
        phone_number=supplier.phone_number,
        street_name=supplier.street_name,
        house_number=supplier.house_number,
        postal_code=supplier.postal_code,
        website=supplier.website,
    )
        # Haal de geüpdatete gegevens op uit het formulier
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.phone_number = form.phone_number.data
        supplier.street_name = form.street_name.data
        supplier.house_number = form.house_number.data
        supplier.postal_code = form.postal_code.data
        supplier.website = form.website.data

        try:
            # Update de leverancier in de database
            supplier.edit()
            flash("Supplier updated successfully!", "success")
            return redirect(url_for("suppliers"))  # Redirect naar leverancierslijst
        except Error as e:
            logger.error(f" A critical error has occurred in  supplier_edit(): {e} ")
            abort(500)

    # Render het formulier met de bestaande gegevens
    return render_template("suppliers/supplier_edit.html", form=form, supplier_id=supplier_id)



@app.route('/orders')
def orders():
    try:
        return render_template("orders/orders.html")
    except Error as e:
        abort(500)
        logger.error(f" A critical error has occurred in  orders(): {e} ")
        
        
@app.route('/orders/<int:order_id>')

def order_details(order_id):
    
    
    order = Order.get_order_by_id(order_id)
    if not order:
        abort(404)
        
    totale = Order.get_order_total_by_id(order_id)
    
    customer = Order.get_order_customer_info_by_id(order_id)
    
    order_lines = Order.get_order_lines_by_id(order_id)
    
    # order = {
    #     "order_number": 1,
    #     "customer_name": "yazan sweed",
    #     "total": 37.39,
    #     "payment_status": "Not Paid",
    #     "status_options": ["New", "In Progress", "Sent", "Delivered", "Canceled"],
    #     "current_status": "In Progress",
    #     "invoice_address": {
    #         "company_name": "",
    #         "email": "admin@gmail.com",
    #         "phone": "0612345678",
    #         "street": "koolhoensraat",
    #         "house_number": "3",
    #         "postal_code": "6035 GO",
    #         "place": "opel",
    #         "country": "Nederland"
    #     },
    #     "shipping_address": {
    #         "company_name": "",
    #         "email": "admin@gmail.com",
    #         "phone": "0612345678",
    #         "street": "koolhoensraat",
    #         "house_number": "3",
    #         "postal_code": "6035 GO",
    #         "place": "opel",
    #         "country": "Nederland"
    #     },
    #     "order_items": [
    #         {
    #             "id": 1,
    #             "product_name": "Monseame Senger",
    #             "status": "In behandeling",
    #             "price": 9.12,
    #             "amount": 5,
    #             "total": 45.60
    #         }
    #     ]
    # }
    
    
    
    return render_template('orders/order_details.html', order=order , order_lines=order_lines , customer=customer , totale=totale)


    

@app.route("/customers")
def customers():
    try:
        return render_template("customers/customers.html")
    except Error as e:
        logger.error(f" A critical error has occurred in  customers(): {e} ")
        abort(500)



@app.route("/customers/<int:customer_id>")
def customer_view(customer_id):
    try:
        customer = Customer.get_by_id(customer_id)
        if not customer:
            abort(404)
            
        return render_template("customers/customer_view.html", customer=customer)
    except Error as e:
        logger.error(f" A critical error has occurred in  customer_view(): {e} ")
        abort(500)


@app.route("/customers/edit/<int:customer_id>", methods=["GET", "POST"])
def customer_edit(customer_id):
    customer = Customer.get_by_id(customer_id)
    if not customer:
        abort(404)
    form = EditCustomerForm(
        customer_id=customer.customerID,
        name=customer.name,
        phone_number=customer.phone_number,
        email=customer.email,
        street_name=customer.street_name,
        house_number=customer.house_number,
        postal_code=customer.postal_code,
        city=customer.city,
        
    ) 
    
    print(form.customer_id.data)
    # Vul het formulier met bestaande klantgegevens
    if form.validate_on_submit():
        # Werk de klantgegevens bij met de gegevens uit het formulier
        
        customer.name = form.name.data
        customer.phone_number = form.phone_number.data
        customer.email = form.email.data
        customer.street_name = form.street_name.data
        customer.house_number = form.house_number.data
        customer.postal_code = form.postal_code.data
        customer.city = form.city.data

        try:
            customer.edit()
            return redirect(url_for("customers"))
        except Error as e:
            logger.error(f" A critical error has occurred in  customer_edit(): {e} ")
            abort(500)

    return render_template("customers/customer_edit.html", form=form, customer_id=customer_id)




@app.route("/customers/create", methods=["GET", "POST"])
def customer_create():
    form = CustomerForm()
    if form.validate_on_submit():
        # Maak een nieuwe klant aan met de gegevens uit het formulier
        new_customer = Customer(
            name=form.name.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            street_name=form.street_name.data,
            house_number=form.house_number.data,
            postal_code=form.postal_code.data,
            city=form.city.data,
        )
        try:
            new_customer.create()
            return redirect(url_for("customers"))
        except Error as e:
            logger.error(f" A critical error has occurred in  customer_create(): {e} ")
            abort(500)

    return render_template("customers/customer_create.html", form=form)




@app.route("/cart")
def cart():
    
    try:
        orderID = session.get('orderID')
        if not orderID:
            customer_name = ""
        else:
            customer_name = Order.get_customer_name_by_orderID(orderID)
    
        return render_template("cart/cart.html" , customer_name=customer_name)

    except Error as e:
        logger.error(f" A critical error has occurred in  cart(): {e} ")
        abort(500)
    



def generate_tracking_code():
    while True:
        prefix = "TATC_"
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        track_code = prefix + random_part
        
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM orders where tracking_code = %s"
        cursor.execute(query, (track_code,))
        exists = cursor.fetchone()
        if not exists:
            return track_code
        
        cursor.close()
        connection.close()
        
        
    

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    
    orderID = session.get('orderID')
    
    
        
    if not orderID:
            return redirect(url_for('cart'))
        
    is_order_lins = Order.check_if_order_lins_by_id(orderID)
    if not is_order_lins:
        return redirect(url_for('cart'))
    form = CheckoutForm()

    # Tracking code genereren en aan het formulier toevoegen
    if request.method == 'GET':
        form.tracking_code.data = generate_tracking_code()

    if form.validate_on_submit():
       
        orderID = session.get('orderID')
        date = form.date.data
        delivery_time = form.delivery_time.data
        tracking_code = form.tracking_code.data
        urgent = form.urgent.data
        delivery_postal_code = form.delivery_postal_code.data
        delivery_house_number = form.delivery_house_number.data
        delivery_city = form.delivery_city.data
        
        try:
            
            Order.update_order(orderID, date, delivery_time, tracking_code, urgent, delivery_postal_code, delivery_house_number, delivery_city)
            Order.update_stock(orderID)

            session.pop('orderID')
            
            return redirect(url_for('cart'))
            
        except Error as e:
            logger.error(f" A critical error has occurred in  checkout(): {e} ")
            abort(500)
            
        
        
        if not orderID:
            abort(503)
          
    return render_template('checkout.html', form=form)


@app.route("/invoice")
def invoice():
    
    
    session['orderID'] = 1
    
    orderID=  session.get('orderID')
    print(session.get('orderID'))
    
    return f" Invoice page  { orderID }"
    




@app.route("/send-email")
def send_email():

    customer_name = request.form.get("name")
    invoice_details = {
        "item": "Product A",
        "quantity": 2,
        "price": 50.0,
        "total": 100.0,
    }

    # Render the invoice template as HTML
    html_invoice = render_template("invoice.html", name=customer_name, details=invoice_details)

    # Send email
    subject = "Your Invoice"
    msg = Message(
        subject,
        recipients=["avans1@mohmadyazansweed.nl", "yazn.sweed2001@gmail.com"],
    )
    msg.html = html_invoice
    mail.send(msg)

    return "E-mail verzonden!"







@app.errorhandler(404) 
def page_not_found(e):
    return render_template('errors/404.html'), 404



@app.errorhandler(503) 
def page_not_found(e):
    return render_template('errors/503.html'), 503


@app.errorhandler(500) 
def page_not_found(e):
    return render_template('errors/500.html'), 500