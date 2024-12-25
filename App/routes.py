from flask import Flask, redirect, url_for, request, render_template, jsonify , flash
from app import app, mail
import mysql.connector
from mysql.connector import Error
from App.classes.products import Product
from App.classes.suppliers import Supplier
from flask_mail import Message
from flask import session
import random

from App.form.productform import ProductForm



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

def calculate_co2_truck(distance_km, emission_per_km=900):          
    total_grams = distance_km * emission_per_km
    total_kg = total_grams / 1000  # Convert to kilograms
    return total_kg


@app.route("/Dashboard")
@app.route("/")
def dashboard():
    standard_co2 = calculate_co2_truck(random.randint(100, 500))
    express_co2 = calculate_co2_truck(random.randint(100, 500)+200)
    
        
    connection = create_connection()
    if not connection:
        return render_template("dashboard.html" , products = [] , standard_co2 = standard_co2 , express_co2 = express_co2)
        #return jsonify({"error": "Geen verbinding met database"}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT p.productID , p.name , p.stock , p.minimum_stock   FROM products p  where stock  <= minimum_stock ")  # Pas de tabelnaam aan 
        rows = cursor.fetchall()

        products = [Product(row['productID'], row['name'] , row['stock'] , row['minimum_stock'] ,) for row in rows]
        return render_template('dashboard.html', products=products , standard_co2 = standard_co2 , express_co2 = express_co2)
       # return jsonify([t.__dict__ for t in products])

    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()




@app.route("/products")
def products():
        
        try:
            
            products = Product.get_all()
            
            
            # page = request.args.get(
            #     "page", 1, type=int
            # )  # Default to page 1 if not specified
            # per_page = 10
            # strat = (page - 1) * per_page
            # end = strat + per_page
            # total_pages = (len(products) + per_page - 1) // per_page
            # print(total_pages)
            # products = products[strat:end]
            return render_template(
                "products/products.html", products=products
            )
            # return render_template(
            #     "products.html", products=products, total_pages=total_pages, page=page
            # )
            # return jsonify([t.__dict__ for t in products])

        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            print("Done")
            # cursor.close()
            # connection.close()


@app.route("/products/<product_id>")
def product(product_id):
    product = Product.get_by_id(product_id)
 
    suppliers = product.get_suppliers()
    return render_template("products/product_view.html", product=product , suppliers = suppliers)
        
@app.route('/products/create', methods=['GET', 'POST'])
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            productID=form.productID.data,
            name=form.name.data,
            article_number=form.article_number.data,
            stock=form.stock.data,
            minimum_stock=form.minimum_stock.data,
            perishable=form.perishable.data,
            adviceID=form.adviceID.data,
            energy_cost=form.energy_cost.data,
            packaging_size=form.packaging_size.data,
            storage_locationID=form.storage_locationID.data,
            suppliers=form.suppliers.data
        )
        
        
        for supplier in form.suppliers.data:
            print(supplier)
        
      
        flash(f"Product {product.name} aangemaakt met ID {product.productID}", 'success')
        return redirect(url_for('products'))

    return render_template('products/product_create_form.html', form=form)




@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Simulated database call to get product details
    product_details = {
        "productID": product_id,
        "name": "Example Product",
        "article_number": "12345",
        "stock": 50,
        "minimum_stock": 10,
        "perishable": True,
        "adviceID": "2",
        "energy_cost": 25.5,
        "packaging_size": "Medium",
        "storage_locationID": "1",
        "suppliers": ["1", "3"]
    }

    form = ProductForm(data=product_details)

    if form.validate_on_submit():
        updated_product = Product(
            productID=form.productID.data,
            name=form.name.data,
            article_number=form.article_number.data,
            stock=form.stock.data,
            minimum_stock=form.minimum_stock.data,
            perishable=form.perishable.data,
            adviceID=form.adviceID.data,
            energy_cost=form.energy_cost.data,
            packaging_size=form.packaging_size.data,
            storage_locationID=form.storage_locationID.data,
            suppliers=form.suppliers.data
        )
        flash(f"Product {updated_product.name} updated successfully.", 'success')
        return redirect(url_for('products'))

    return render_template('products/product_edit_form.html', form=form, product_id=product_id)


@app.route("/suppliers")
def suppliers():
    
    try:
        suppliers = Supplier.get_all()
        return render_template(
            "suppliers/suppliers.html", suppliers=suppliers
        )
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        print("Done")
        # cursor.close()
        # connection.close()
    


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
    html_invoice = render_template(
        "invoice.html", name=customer_name, details=invoice_details
    )

    # Send email
    subject = "Your Invoice"
    msg = Message(
        subject, recipients=["avans1@mohmadyazansweed.nl", "yazn.sweed2001@gmail.com"]
    )
    msg.html = html_invoice
    mail.send(msg)

    return "E-mail verzonden!"




