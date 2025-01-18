from flask import (
    Flask,
    redirect,
    url_for,
    request,
    jsonify,
    session,
    flash,
)
from app import app, mail
import mysql.connector
from mysql.connector import Error
from App.classes.products import Product
from App.classes.suppliers import Supplier
from flask_mail import Message
import random
from logging_config import logger
from App.classes.orders import Order


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
        logger.error(f"Error connecting to the database in create_connection: {e}")
        return None





@app.route("/api/dashboard_products", methods=["POST", "GET"])
def api_dashboard_products():
    connection = create_connection()
    if not connection:
        logger.error("Failed to establish a database connection in api_products")
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        if request.method == "POST":
            draw = request.form["draw"]
            row = int(request.form["start"])
            rowperpage = int(request.form["length"])
            searchValue = request.form["search[value]"]

            cursor.execute("SELECT count(*) as allcount FROM products where stock  <= minimum_stock")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"]

            likeString = "%" + searchValue + "%"
            cursor.execute(
                "SELECT count(*) as allcount FROM products where stock  <= minimum_stock and (name LIKE %s OR productID LIKE %s OR article_number LIKE %s)",
                (likeString, likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"]

            if searchValue == "":
                cursor.execute(
                    "SELECT * FROM products where stock  <= minimum_stock  ORDER BY productID ASC LIMIT %s, %s",
                    (row, rowperpage),
                )
            else:
                cursor.execute(
                    "SELECT * FROM products where stock  <= minimum_stock  and (name LIKE %s OR productID LIKE %s OR article_number LIKE %s) ORDER BY productID ASC LIMIT %s, %s",
                    (likeString, likeString, likeString, row, rowperpage),
                )

            productslist = cursor.fetchall()
            data = [
                {
                    "productID": row["productID"],
                    "name": row["name"],
                    "article_number": row["article_number"],
                    "stock": row["stock"],
                    "minimum_stock": row["minimum_stock"],
                    "price": row["price"],
                }
                for row in productslist
            ]

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        logger.error(f"Error in api_products: {e}, Request Data: {request.form}")
        return jsonify({"error": "An error occurred while fetching products"}), 500
    finally:
        cursor.close()
        connection.close()






@app.route("/api/products", methods=["POST", "GET"])
def api_products():
    connection = create_connection()
    if not connection:
        logger.error("Failed to establish a database connection in api_products")
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        if request.method == "POST":
            draw = request.form["draw"]
            row = int(request.form["start"])
            rowperpage = int(request.form["length"])
            searchValue = request.form["search[value]"]

            cursor.execute("SELECT count(*) as allcount FROM products")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"]

            likeString = "%" + searchValue + "%"
            cursor.execute(
                "SELECT count(*) as allcount FROM products WHERE name LIKE %s OR productID LIKE %s OR article_number LIKE %s",
                (likeString, likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"]

            if searchValue == "":
                cursor.execute(
                    "SELECT * FROM products ORDER BY productID ASC LIMIT %s, %s",
                    (row, rowperpage),
                )
            else:
                cursor.execute(
                    "SELECT * FROM products WHERE name LIKE %s OR productID LIKE %s OR article_number LIKE %s ORDER BY productID ASC LIMIT %s, %s",
                    (likeString, likeString, likeString, row, rowperpage),
                )

            productslist = cursor.fetchall()
            data = [
                {
                    "productID": row["productID"],
                    "name": row["name"],
                    "article_number": row["article_number"],
                    "stock": row["stock"],
                    "minimum_stock": row["minimum_stock"],
                    "price": row["price"],
                }
                for row in productslist
            ]

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        logger.error(f"Error in api_products: {e}, Request Data: {request.form}")
        return jsonify({"error": "An error occurred while fetching products"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route("/api/suppliers", methods=["POST", "GET"])
def api_suppliers():
    connection = create_connection()
    if not connection:
        logger.error("Failed to establish a database connection in api_suppliers")
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        if request.method == "POST":
            draw = request.form["draw"]
            row = int(request.form["start"])
            rowperpage = int(request.form["length"])
            searchValue = request.form["search[value]"]

            cursor.execute("SELECT COUNT(*) as allcount FROM suppliers")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"]

            likeString = "%" + searchValue + "%"
            cursor.execute(
                "SELECT COUNT(*) as allcount FROM suppliers WHERE name LIKE %s OR website LIKE %s OR supplierID LIKE %s",
                (likeString, likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"]

            if searchValue == "":
                cursor.execute(
                    "SELECT * FROM suppliers ORDER BY name ASC LIMIT %s, %s",
                    (row, rowperpage),
                )
            else:
                cursor.execute(
                    "SELECT * FROM suppliers WHERE name LIKE %s OR website LIKE %s OR supplierID LIKE %s LIMIT %s, %s",
                    (likeString, likeString, likeString, row, rowperpage),
                )

            supplierlist = cursor.fetchall()
            data = [
                {
                    "supplierID": row["supplierID"],
                    "name": row["name"],
                    "phone_number": row["phone_number"],
                    "street_name": row["street_name"],
                    "house_number": row["house_number"],
                    "postal_code": row["postal_code"],
                    "website": row["website"],
                }
                for row in supplierlist
            ]

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        logger.error(f"Error in api_suppliers: {e}, Request Data: {request.form}")
        return jsonify({"error": "An error occurred while fetching suppliers"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route("/api/orders", methods=["POST", "GET"])
def api_order():
    connection = create_connection()
    if not connection:
        logger.error("Failed to establish a database connection in api_order")
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        if request.method == "POST":
            draw = int(request.form.get("draw", 0))
            row = int(request.form.get("start", 0))
            rowperpage = int(request.form.get("length", 10))
            searchValue = request.form.get("search[value]", "").strip()

            cursor.execute(
                "SELECT count(*) as allcount FROM orders o INNER JOIN customers c ON c.customerID = o.customerID where o.status != 'making'"
            )
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"] if rsallcount else 0

            likeString = f"%{searchValue}%"
            cursor.execute(
                """
                SELECT COUNT(*) as allcount 
                FROM orders o 
                INNER JOIN customers c ON c.customerID = o.customerID  
                WHERE o.status != 'making' and  (c.name LIKE %s OR c.email LIKE %s OR o.orderID LIKE %s OR o.tracking_code LIKE %s)
                  
                """,
                (likeString, likeString, likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"] if rsallcount else 0

            if searchValue:
                cursor.execute(
                    """
               SELECT o.*, c.name, c.email  
                FROM orders o 
                INNER JOIN customers c ON c.customerID = o.customerID  
                WHERE o.status != 'making' 
                AND (c.name LIKE %s OR c.email LIKE %s OR o.orderID LIKE %s OR o.tracking_code LIKE %s) 
                ORDER BY o.orderID ASC 
                LIMIT %s, %s
                    """,
                    (likeString, likeString, likeString, likeString, row, rowperpage),
                )
            else:
                cursor.execute(
                    """
                    SELECT o.*, c.name, c.email  
                    FROM orders o 
                    INNER JOIN customers c ON c.customerID = o.customerID   
                    WHERE o.status != 'making'
                    ORDER BY o.orderID ASC 
                    LIMIT %s, %s
                    """,
                    (row, rowperpage),
                )

            employeelist = cursor.fetchall()
            data = [
                {
                    "orderID": record["orderID"],
                    "name": record["name"],
                    "email": record["email"],
                    "status": record["status"],
                    "date": record["date"],
                }
                for record in employeelist
            ]

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        logger.error(f"Error in api_order: {e}, Request Data: {request.form}")
        return jsonify({"error": "An error occurred while fetching orders"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route("/api/customers", methods=["POST", "GET"])
def api_customers():
    connection = create_connection()
    if not connection:
        logger.error("Failed to establish a database connection in api_customers")
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        if request.method == "POST":
            draw = request.form["draw"]
            row = int(request.form["start"])
            rowperpage = int(request.form["length"])
            searchValue = request.form["search[value]"]

            cursor.execute("SELECT COUNT(*) as allcount FROM customers")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"]

            likeString = "%" + searchValue + "%"
            cursor.execute(
                "SELECT COUNT(*) as allcount FROM customers WHERE name LIKE %s OR email LIKE %s OR customerID LIKE %s OR phone_number LIKE %s",
                (likeString, likeString, likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"]

            if searchValue == "":
                cursor.execute(
                    "SELECT * FROM customers ORDER BY customerID ASC LIMIT %s, %s",
                    (row, rowperpage),
                )
            else:
                cursor.execute(
                    "SELECT * FROM customers WHERE name LIKE %s OR email LIKE %s OR customerID LIKE %s OR phone_number LIKE %s ORDER BY customerID ASC LIMIT %s, %s",
                    (likeString, likeString, likeString, likeString, row, rowperpage),
                )

            customerlist = cursor.fetchall()
            data = [
                {
                    "customerID": row["customerID"],
                    "name": row["name"],
                    "phone_number": row["phone_number"],
                    "email": row["email"],
                    "street_name": row["street_name"],
                    "house_number": row["house_number"],
                    "postal_code": row["postal_code"],
                    "city": row["city"],
                    "annual_revenue": row["annual_revenue"],
                    "customer_discount": row["customer_discount"],
                }
                for row in customerlist
            ]

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        logger.error(f"Error in api_customers: {e}, Request Data: {request.form}")
        return jsonify({"error": "An error occurred while fetching customers"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route("/api/orders/create/<int:customerID>", methods=["POST"])
def create_order(customerID):
    if not customerID:
        logger.error("Customer ID not provided in create_order")
        return jsonify({"error": "Customer ID is required"}), 400

    try:
        orderID = Order.create_order_by_customerID(customerID)
        session["orderID"] = orderID
        logger.info(
            f"Order created successfully: OrderID={orderID}, CustomerID={customerID}"
        )
        return (
            jsonify(
                {
                    "message": "Order created successfully",
                    "customer_id": customerID,
                    "orderID": orderID,
                }
            ),
            201,
        )
    except Exception as e:
        logger.error(f"Error in create_order: {e}, CustomerID: {customerID}")
        return (
            jsonify(
                {
                    "error": "An error occurred while creating the order",
                    "details": str(e),
                }
            ),
            500,
        )


@app.route("/api/session/order", methods=["GET"])
def get_session_order():
    try:
        orderID = session.get("orderID")
        if orderID:
            return jsonify({"orderID": orderID}), 200
        logger.warning("No order found in session")
        return jsonify({"orderID": None}), 200
    except Exception as e:
        logger.error(f"Error in get_session_order: {e}")
        return (
            jsonify({"error": "An error occurred while retrieving the session order"}),
            500,
        )


@app.route("/api/cart_items")
def get_cart():
    orderID = session.get("orderID")
    if not orderID:
        logger.error("No order found in session in get_cart")
        return jsonify({"error": "No order found"}), 404

    connection = create_connection()
    if not connection:
        logger.error("Failed to establish a database connection in get_cart")
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT  p.name, p.stock, o.order_lineID, o.quantity, o.price 
            FROM order_lines o
            INNER JOIN products p ON p.productID = o.productID
            WHERE o.orderID = %s
            """,
            (orderID,),
        )
        cart_items = cursor.fetchall()

        if not cart_items:
            logger.warning(f"No items found in cart for OrderID: {orderID}")
            return jsonify(data=[])

        cursor.execute(
            """
            SELECT  discount
            FROM orders
            WHERE orderID = %s
            """,
            (orderID,),
        )

        discount = cursor.fetchone()

        data = [
            {
                "name": row["name"],
                "stock": row["stock"],
                "order_lineID": row["order_lineID"],
                "quantity": row["quantity"],
                "price": row["price"],
            }
            for row in cart_items
        ]

        return jsonify({"cart": data, "discount": discount["discount"]}), 200

    except Exception as e:
        logger.error(f"Error in get_cart: {e}, OrderID: {orderID}")
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching the cart items",
                    "details": str(e),
                }
            ),
            500,
        )
    finally:
        cursor.close()
        connection.close()


@app.route("/api/cart/add", methods=["POST"])
def add_order_line():
    connection = create_connection()

    if not connection:
        logger.error("Failed to establish a database connection in add_order_line")
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        data = request.get_json()

        # Extract fields from the request
        orderID = session.get("orderID")
        productID = data.get("productID")
        quantity = int(data.get("quantity"))
        logger.info(
            f"Adding order line: orderID={orderID}, productID={productID}, quantity={quantity}"
        )

        cursor = connection.cursor(dictionary=True)

        check_product_query = """
            SELECT stock , price FROM products WHERE productID = %s
        """
        cursor.execute(check_product_query, (productID,))
        product = cursor.fetchone()

        if not product:
            logger.error(f"Product not found for productID: {productID}")
            return jsonify({"error": "Product not found"}), 404

        stock = product["stock"]
        price = product["price"]

        # Check required fields
        if not all([orderID, productID, quantity, price]):
            logger.error("Missing required fields in add_order_line")
            return jsonify({"error": "Missing required fields"}), 400

        # Validate values
        if quantity <= 0 or price <= 0:
            logger.error("Invalid quantity or price in add_order_line")
            return jsonify({"error": "Quantity and price must be greater than 0"}), 400

        if quantity > stock:
            logger.error(f"Requested quantity exceeds stock for productID: {productID}")
            return jsonify({"error": "Quantity is greater than stock"}), 400

        # Check if the product already exists in the order
        check_query = """
            SELECT order_lineID, quantity
            FROM order_lines
            WHERE orderID = %s AND productID = %s
        """
        cursor.execute(check_query, (orderID, productID))
        existing_row = cursor.fetchone()

        if existing_row:
            total_quantity = existing_row["quantity"] + quantity

            if total_quantity > stock:
                logger.warning(
                    f"Updating quantity to stock limit for productID: {productID}"
                )
                update_query = """
                    UPDATE order_lines
                    SET quantity = %s, price = %s
                    WHERE order_lineID = %s
                """
                cursor.execute(
                    update_query, (stock, price, existing_row["order_lineID"])
                )
            else:
                update_query = """
                    UPDATE order_lines
                    SET quantity = quantity + %s, price = %s
                    WHERE order_lineID = %s
                """
                cursor.execute(
                    update_query, (quantity, price, existing_row["order_lineID"])
                )
            connection.commit()

            logger.info(
                f"Order line updated successfully for orderID: {orderID}, productID: {productID}"
            )
            return (
                jsonify(
                    {
                        "message": "Order line updated successfully",
                        "order_line": {
                            "order_lineID": existing_row["order_lineID"],
                            "orderID": orderID,
                            "productID": productID,
                            "quantity": total_quantity,
                            "price": price,
                        },
                    }
                ),
                201,
            )

        # Product does not exist -> add a new order line
        insert_query = """
            INSERT INTO order_lines (orderID, productID, quantity, price)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (orderID, productID, quantity, price))
        connection.commit()
        logger.info(
            f"Order line added successfully: orderID={orderID}, productID={productID}, quantity={quantity}"
        )
        return (
            jsonify(
                {
                    "message": "Order line added successfully",
                    "order_line": {
                        "order_lineID": cursor.lastrowid,
                        "orderID": orderID,
                        "productID": productID,
                        "quantity": quantity,
                        "price": price,
                    },
                }
            ),
            201,
        )

    except Error as e:
        logger.error(f"Database error in add_order_line: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if connection.is_connected():
            connection.close()


@app.route("/api/cart/remove", methods=["POST"])
def remove_order_line():
    connection = create_connection()

    if not connection:
        logger.error("Failed to establish a database connection in remove_order_line")
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        data = request.get_json()

        # Extract fields from the request
        order_lineID = data.get("order_lineID")
        logger.info(f"Removing order line: order_lineID={order_lineID}")

        if not order_lineID:
            logger.error("Missing order_lineID in remove_order_line")
            return jsonify({"error": "order_lineID is required"}), 400

        cursor = connection.cursor(dictionary=True)

        delete_query = """
            DELETE FROM order_lines WHERE order_lineID = %s
        """
        cursor.execute(delete_query, (order_lineID,))
        connection.commit()

        if cursor.rowcount == 0:
            logger.warning(f"No order line found with order_lineID: {order_lineID}")
            return jsonify({"error": "Order line not found"}), 404

        logger.info(f"Order line removed successfully: order_lineID={order_lineID}")
        return jsonify({"message": "Order line removed successfully"}), 200

    except Error as e:
        logger.error(f"Database error in remove_order_line: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if connection.is_connected():
            connection.close()
            logger.info("Database connection closed in remove_order_line")


@app.route("/api/cart/update", methods=["POST"])
def update_order_line():
    connection = create_connection()

    if not connection:
        logger.error("Failed to establish a database connection in update_order_line")
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        data = request.get_json()

        # Extract fields from the request
        order_lineID = data.get("order_lineID")
        quantity = data.get("quantity")
        logger.info(
            f"Updating order line: order_lineID={order_lineID}, quantity={quantity}"
        )

        if not all([order_lineID, quantity]):
            logger.error("Missing required fields in update_order_line")
            return jsonify({"error": "order_lineID and quantity are required"}), 400

        if quantity <= 0:
            logger.error(f"Invalid quantity in update_order_line: {quantity}")
            return jsonify({"error": "Quantity must be greater than 0"}), 400

        cursor = connection.cursor(dictionary=True)

        # Validate the order line exists
        check_query = """
            SELECT order_lineID, productID, quantity 
            FROM order_lines 
            WHERE order_lineID = %s
        """
        cursor.execute(check_query, (order_lineID,))
        order_line = cursor.fetchone()

        if not order_line:
            logger.error(f"No order line found with order_lineID: {order_lineID}")
            return jsonify({"error": "Order line not found"}), 404

        # Validate stock availability
        cursor.execute(
            "SELECT stock FROM products WHERE productID = %s",
            (order_line["productID"],),
        )
        product = cursor.fetchone()
        if not product or quantity > product["stock"]:
            logger.error(
                f"Requested quantity exceeds stock for productID: {order_line['productID']}"
            )
            return jsonify({"error": "Quantity exceeds stock"}), 400

        # Update the order line
        update_query = """
            UPDATE order_lines 
            SET quantity = %s 
            WHERE order_lineID = %s
        """
        cursor.execute(update_query, (quantity, order_lineID))
        connection.commit()

        logger.info(
            f"Order line updated successfully: order_lineID={order_lineID}, quantity={quantity}"
        )
        return jsonify({"message": "Order line updated successfully"}), 200

    except Error as e:
        logger.error(f"Database error in update_order_line: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if connection.is_connected():
            connection.close()
            logger.info("Database connection closed in update_order_line")


@app.route("/api/cart/clear", methods=["POST"])
def clear_cart():
    connection = create_connection()

    if not connection:
        logger.error("Failed to establish a database connection in clear_cart")
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        orderID = session.get("orderID")
        logger.info(f"Clearing cart for orderID: {orderID}")

        if not orderID:
            logger.error("No orderID found in session for clear_cart")
            return jsonify({"error": "No active order found"}), 400

        cursor = connection.cursor(dictionary=True)

        clear_query = """
            DELETE FROM order_lines WHERE orderID = %s
        """
        cursor.execute(clear_query, (orderID,))
        connection.commit()

        logger.info(f"Cart cleared successfully for orderID: {orderID}")
        return jsonify({"message": "Cart cleared successfully"}), 200

    except Error as e:
        logger.error(f"Database error in clear_cart: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if connection.is_connected():
            connection.close()
            logger.info("Database connection closed in clear_cart")


@app.route("/api/cart/cancel", methods=["POST"])
def cancel_cart():
    connection = create_connection()

    if not connection:
        logger.error("Failed to establish a database connection in cancel_cart")
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        orderID = session.get("orderID")
        logger.info(f"Cancelling cart for orderID: {orderID}")

        if not orderID:
            logger.error("No orderID found in session for cancel_cart")
            return jsonify({"error": "No active order found"}), 400

        cursor = connection.cursor(dictionary=True)

        # Remove all order lines
        delete_lines_query = """
            DELETE FROM order_lines WHERE orderID = %s
        """
        cursor.execute(delete_lines_query, (orderID,))

        # Remove the order itself
        delete_order_query = """
            DELETE FROM orders WHERE orderID = %s
        """
        cursor.execute(delete_order_query, (orderID,))
        connection.commit()

        session.pop("orderID", None)  # Remove orderID from session

        logger.info(f"Cart and order cancelled successfully for orderID: {orderID}")
        return jsonify({"message": "Cart and order cancelled successfully"}), 200

    except Error as e:
        logger.error(f"Database error in cancel_cart: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if connection.is_connected():
            connection.close()
            logger.info("Database connection closed in cancel_cart")
