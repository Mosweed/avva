from App import app
from App.classes.db import db
import mysql.connector
from mysql.connector import Error


class Order(db):
    # this class is used to interact with the orders table in the database the orders table has the following columns
    # orderID, customerID, date , delivery_time , status , discount ,tracking_code , urgent ,  delivery_city , delivery_postcode  ,  delivery_house_number.

    def __init__(
        self,
        orderID=None,
        customerID=None,
        date=None,
        delivery_time=None,
        status=None,
        discount=None,
        tracking_code=None,
        urgent=None,
        delivery_city=None,
        delivery_postcode=None,
        delivery_house_number=None,
    ):
        self.orderID = orderID
        self.customerID = customerID
        self.date = date
        self.delivery_time = delivery_time
        self.status = status
        self.discount = discount
        self.tracking_code = tracking_code
        self.urgent = urgent
        self.delivery_city = delivery_city
        self.delivery_postcode = delivery_postcode
        self.delivery_house_number = delivery_house_number

    @staticmethod
    def create_order_by_customerID(customerID):
        """Create a new order in the database"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                INSERT INTO `orders`(`customerID`, `discount`)VALUES( %s ,(select customer_discount from customers where customerID = %s) );
                """
                cursor.execute(query , (customerID,customerID,))
                connection.commit()
                orderID = cursor.lastrowid
                return orderID
            except Error as e:
                print(f"Error during order creation: {e}")
            finally:
                cursor.close()
                connection.close()


    @staticmethod
    def get_customer_name_by_orderID(orderID):
        """Get the customer name by orderID"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    Select c.name from orders o inner join customers c
                    on o.customerID = c.customerID
                    where o.orderID = %s;
                """
                cursor.execute(query , (orderID,))
                customer = cursor.fetchall()
                customer_name = customer[0][0]
                
                if customer:
                    return customer_name
                else:
                    return None
                
                
            except Error as e:
                print(f"Error during customer information retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
                


    @staticmethod
    def update_order(orderID, date, delivery_time, tracking_code, urgent, delivery_postal_code, delivery_house_number, delivery_cit):
        """Update the order information"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                UPDATE `orders` 
                    SET `status` = 'processing', 
                        `date` = %s, 
                        `delivery_time` = %s, 
                        `tracking_code` = %s, 
                        `urgent` = %s, 
                        `delivery_postal_code` = %s, 
                        `delivery_house_number` = %s, 
                        `delivery_city` = %s 
                    WHERE `orderID` = %s;

                """
                cursor.execute(query, (date, delivery_time, tracking_code, urgent, delivery_postal_code, delivery_house_number, delivery_cit, orderID))
                connection.commit()
            except Error as e:
                print(f"Error during order update: {e}")
            finally:
                cursor.close()
                connection.close()
                
                

    @staticmethod
    def update_stock (orderID):
        """Update the stock in the database"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                UPDATE products p
                INNER JOIN order_lines ol
                ON p.productID = ol.productID
                SET p.stock = p.stock - ol.quantity
                WHERE ol.orderID = %s;
                """
                cursor.execute(query, (orderID,))
                connection.commit()
            except Error as e:
                print(f"Error during stock update: {e}")
            finally:
                cursor.close()
                connection.close()
                
                

    @staticmethod
    def check_if_order_lins_by_id(orderID):
        """Get the order lines by orderID"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT *
                FROM order_lines ol
                WHERE ol.orderID = %s;
                """
                cursor.execute(query, (orderID,))
                order_lines = cursor.fetchall()
                if order_lines:
                    return True
                else:
                    return False
            except Error as e:
                print(f"Error during order lines retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
                

    @staticmethod
    def get_order_by_id(orderID):
        """Get the order by orderID"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = """
                SELECT * FROM orders WHERE orderID = %s;
                """
                cursor.execute(query, (orderID,))
                rows = cursor.fetchall()
                order = {}
                if rows:
                    
                    for row in rows:
                        order = {
                            "orderID": row["orderID"],
                            "customerID": row["customerID"],
                            "date": row["date"],
                            "delivery_time": row["delivery_time"],
                            "status": row["status"],
                            "discount": row["discount"],
                            "tracking_code": row["tracking_code"],
                            "urgent": row["urgent"],
                            "delivery_city": row["delivery_city"],
                            "delivery_postal_code": row["delivery_postal_code"],
                            "delivery_house_number": row["delivery_house_number"],
                        }
                        
                        return order
                    
                else:
                    return None
            except Error as e:
                print(f"Error during order retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
                
    @staticmethod
    def get_order_lines_by_id(orderID):
        """Get the order lines by orderID"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = """
                SELECT ol.* , p.name  FROM order_lines ol
            INNER JOIN products p ON p.productID = ol.productID
            WHERE ol.orderID =  %s;
                """
                cursor.execute(query, (orderID,))
                rows = cursor.fetchall()
                order_lines = []
                if rows:
                    
                    for row in rows:
                        order_line = {
                            "order_lineID": row["order_lineID"],
                            "orderID": row["orderID"],
                            "productID": row["productID"],
                            "price": row["price"],
                            "quantity": row["quantity"],
                            "name": row["name"],
                        }
                        order_lines.append(order_line)
                    return order_lines
                    
                else:
                    return None
            except Error as e:
                print(f"Error during order lines retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
                
                
    @staticmethod
    def get_order_customer_info_by_id(orderID):
        """Get the order customer information by orderID"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = """
                SELECT c.*
                FROM customers c
                INNER JOIN orders o
                ON c.customerID = o.customerID
                WHERE o.orderID = %s;
                """
                cursor.execute(query, (orderID,))
                
                rows = cursor.fetchall()
                customer_info = {}
                if rows:
                    for row in rows:
                        customer_info = {
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
                    return customer_info 
            
                else:
                    return None
            except Error as e:
                print(f"Error during customer information retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
                
                
    @staticmethod
    def get_order_total_by_id(orderID):
        """Get the order total by orderID"""
        connection = Order.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = """
                SELECT SUM(ol.price * ol.quantity) AS total
                FROM  order_lines ol
                WHERE ol.orderID = %s;
                """
                cursor.execute(query, (orderID,))
                order_total = cursor.fetchall()
                if order_total:
                    return order_total
                else:
                    return None
            except Error as e:
                print(f"Error during order total retrieval: {e}")
            finally:
                cursor.close()
                connection.close()