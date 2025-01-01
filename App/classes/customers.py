import mysql.connector
from mysql.connector import Error
from App.classes.db import db



class Customer(db):

    def __init__(self, customerID=None, name=None, phone_number=None, email=None, street_name=None,
                 house_number=None, postal_code=None, city=None, annual_revenue=None, customer_discount=None):
        self.customerID = customerID
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.street_name = street_name
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.annual_revenue = annual_revenue
        self.customer_discount = customer_discount

  

    def validate(self):
        """ Validate customer fields """
        if not self.name or len(self.name) < 2:
            raise ValueError("Customer name must be at least 2 characters long.")
        if not self.phone_number or len(self.phone_number) < 7:
            raise ValueError("Invalid phone number.")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address.")
        if not self.postal_code or len(self.postal_code) < 6:
            raise ValueError("Invalid postal code .")

    def create(self):
        """ Create a new customer in the database """
        try:
            self.validate()
        except ValueError as e:
            print(f"Error: {e}")
            return

        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    INSERT INTO customers 
                    (name, phone_number, email, street_name, house_number, postal_code, city , annual_revenue, customer_discount) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )
                """
                cursor.execute(query, (self.name, self.phone_number, self.email, self.street_name,
                                       self.house_number, self.postal_code, self.city ,0 , 0 ))
                connection.commit()
                self.customerID = cursor.lastrowid
            except Error as e:
                print(f"Error during customer creation: {e}")                
            finally:
                cursor.close()
                connection.close()

    def edit(self):
        """ Edit an existing customer in the database """
        if not self.customerID:
            raise ValueError("Cannot edit a customer without a valid customerID.")

        try:
            self.validate()
        except ValueError as e:
            return

        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    UPDATE customers 
                    SET name = %s, phone_number = %s, email = %s, street_name = %s, house_number = %s, 
                        postal_code = %s, city = %s, annual_revenue = %s, customer_discount = %s
                    WHERE customerID = %s
                """
                cursor.execute(query, (self.name, self.phone_number, self.email, self.street_name,
                                       self.house_number, self.postal_code, self.city, self.annual_revenue, self.customer_discount, self.customerID))
                connection.commit()
            except Error as e:
                print(f"Error during customer update: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(customerID):
        """ Fetch a customer by its ID """
        connection = Customer.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = "SELECT * FROM customers WHERE customerID = %s"
                cursor.execute(query, (customerID,))
                row = cursor.fetchone()
                if row:
                    return Customer(**row)
            except Error as e:
                print(f"Error during customer retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
        return None

    @staticmethod
    def get_all():
        """ Fetch all customers """
        connection = Customer.create_connection()
        customers = []
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = "SELECT * FROM customers ORDER BY customerID"
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    customers.append(Customer(**row))
                return customers
            except Error as e:
                print(f"Error during customer retrieval: {e}")
            finally:
                cursor.close()
                connection.close()
        return []
