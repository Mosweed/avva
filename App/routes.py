from flask import (
    Flask,
    redirect,
    url_for,
    request,
    render_template,
    jsonify,
    flash,
)
from app import app, mail
import mysql.connector
from mysql.connector import Error
from App.classes.products import Product
from App.classes.suppliers import Supplier
from flask_mail import Message
from flask import session
import random
import string
from App.form.productform import ProductForm, EditProductForm


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
    express_co2 = calculate_co2_truck(random.randint(100, 500) + 200)

    connection = create_connection()
    if not connection:
        return render_template(
            "dashboard.html",
            products=[],
            standard_co2=standard_co2,
            express_co2=express_co2,
        )
        # return jsonify({"error": "Geen verbinding met database"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT p.productID , p.name , p.stock , p.minimum_stock   FROM products p  where stock  <= minimum_stock "
        )  # Pas de tabelnaam aan
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
        return render_template("products/products.html", products=products)
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
    return render_template("products/product_view.html", product=product, suppliers=suppliers)


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
            print(f"Error: {e}")

    return render_template("products/product_create_form.html", form=form)


@app.route("/products/edit/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    # Haal het product op uit de database
    product = Product.get_by_id(product_id)
    if not product:
        flash("Product not found", "danger")
        return redirect(url_for("products"))

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
    }

    # Maak een formulier gebaseerd op deze data
    form = EditProductForm(data=product_data)

    if form.validate_on_submit():
        try:
            # Update product-object met nieuwe data
            product.name = form.name.data
            product.stock = form.stock.data
            product.minimum_stock = form.minimum_stock.data
            product.perishable = form.perishable.data
            product.adviceID = form.adviceID.data
            product.energy_cost = form.energy_cost.data
            product.packaging_size = form.packaging_size.data
            product.storage_locationID = form.storage_locationID.data

            # Pas de wijzigingen toe in de database
            product.edit()

            # Werk de leveranciers bij als dat nodig is
            if form.suppliers.data:
                product.clear_suppliers()
                for supplier_id in form.suppliers.data:
                    print(supplier_id)
                    product.add_supplier(supplier_id)

            flash(f"Product '{product.name}' is succesvol bijgewerkt.", "success")
            return redirect(url_for("products"))
        except Exception as e:
            flash(f"Er is een fout opgetreden: {str(e)}", "danger")

    if form.errors:
        print("Form Errors:", form.errors)

    # Render het formulier als de submit faalt of GET-methode
    return render_template("products/product_edit_form.html", form=form, product_id=product_id)


@app.route("/suppliers")
def suppliers():

    try:
        suppliers = Supplier.get_all()
        return render_template("suppliers/suppliers.html", suppliers=suppliers)

    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        print("Done")
        # cursor.close()
        # connection.close()


@app.route("/suppliers/<int:supplier_id>")
def supplier_view(supplier_id):
    print(supplier_id)
    try:
        # Haal de specifieke leverancier op
        supplier = Supplier.get_by_id(supplier_id)
        if not supplier:
            return jsonify({"error": "Supplier not found"}), 404

        # Haal producten op die aan de leverancier gekoppeld zijn

        # Render de pagina met supplier details en gekoppelde producten
        return render_template("suppliers/supplier_view.html", supplier=supplier)

    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        print("Done")


@app.route("/suppliers/create", methods=["GET", "POST"])
def supplier_create():
    if request.method == "POST":
        # Print formulierdata
        print(request.form)

        name = request.form.get("name")
        phone_number = request.form.get("phone_number")
        street_name = request.form.get("street_name")
        house_number = request.form.get("house_number")
        postal_code = request.form.get("postal_code")
        website = request.form.get("website")

        print(
            f"Received data: {name}, {phone_number}, {street_name}, {house_number}, {postal_code}, {website}"
        )

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
            return redirect(url_for("suppliers"))
        except Error as e:
            print(f"Error: {e}")
            return jsonify({"error": str(e)}), 500

    return render_template("suppliers/supplier_create.html")


@app.route("/suppliers/edit/<int:supplier_id>", methods=["GET", "POST"])
def supplier_edit(supplier_id):
    # Haal de bestaande gegevens van de leverancier op
    supplier = Supplier.get_by_id(supplier_id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    if request.method == "POST":
        # Haal de geüpdatete gegevens op uit het formulier
        supplier.name = request.form.get("name")
        supplier.phone_number = request.form.get("phone_number")
        supplier.street_name = request.form.get("street_name")
        supplier.house_number = request.form.get("house_number")
        supplier.postal_code = request.form.get("postal_code")
        supplier.website = request.form.get("website")

        try:
            # Update de leverancier in de database
            supplier.edit()
            return redirect(url_for("suppliers"))  # Redirect naar leverancierslijst
        except Error as e:
            print(f"Error: {e}")
            return jsonify({"error": str(e)}), 500

    # Render het formulier met de bestaande gegevens
    return render_template("suppliers/supplier_edit.html", supplier=supplier)


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
