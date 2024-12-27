from App.classes.db import db
from mysql.connector import Error


class Supplier(db):
    def __init__(
        self,
        supplierID=None,
        name=None,
        phone_number=None,
        street_name=None,
        house_number=None,
        postal_code=None,
        website=None,
    ):
        self.supplierID = supplierID
        self.name = name
        self.phone_number = phone_number
        self.street_name = street_name
        self.house_number = house_number
        self.postal_code = postal_code
        self.website = website

    @staticmethod
    def get_by_id(supplierID):
        """Fetch a supplier by its ID"""
        connection = Supplier.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)

            try:
                query = "SELECT * FROM suppliers WHERE supplierID = %s"
                cursor.execute(query, (supplierID,))
                row = cursor.fetchone()
                if row:
                    return Supplier(
                        supplierID=row["supplierID"],
                        name=row["name"],
                        phone_number=row["phone_number"],
                        street_name=row["street_name"],
                        house_number=row["house_number"],
                        postal_code=row["postal_code"],
                        website=row["website"],
                    )
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return None

    @staticmethod
    def get_all():
        """Fetch all suppliers"""
        connection = Supplier.create_connection()
        suppliers = []
        if connection:
            cursor = connection.cursor(dictionary=True)

            try:
                query = "SELECT * FROM suppliers ORDER BY supplierID"
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    supplier = Supplier(
                        supplierID=row["supplierID"],
                        name=row["name"],
                        phone_number=row["phone_number"],
                        street_name=row["street_name"],
                        house_number=row["house_number"],
                        postal_code=row["postal_code"],
                        website=row["website"],
                    )
                    suppliers.append(supplier)

                return suppliers
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return []

    def create(self):
        """Create a new supplier in the database"""
        print(self)
        connection = Supplier.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    INSERT INTO suppliers 
                    (name, phone_number, street_name, house_number, postal_code, website) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        self.name,
                        self.phone_number,
                        self.street_name,
                        self.house_number,
                        self.postal_code,
                        self.website,
                    ),
                )
                connection.commit()
                self.supplierID = cursor.lastrowid
                print(f"Supplier created successfully with ID: {self.supplierID}")
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    def edit(self):
        """Edit an existing supplier in the database"""
        if not self.supplierID:
            print("Error: Cannot edit a supplier without a valid supplierID.")
            return

        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:

                query = """
                    UPDATE suppliers 
                    SET name = %s, phone_number = %s, street_name = %s, house_number = %s, 
                        postal_code = %s, website = %s
                    WHERE supplierID = %s
                """
                cursor.execute(
                    query,
                    (
                        self.name,
                        self.phone_number,
                        self.street_name,
                        self.house_number,
                        self.postal_code,
                        self.website,
                        self.supplierID,
                    ),
                )
                connection.commit()
                print(f"Supplier with ID {self.supplierID} updated successfully!")
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_id_and_name():
        connection = Supplier.create_connection()
        if connection:
            suppliers = []

            cursor = connection.cursor(dictionary=True)
            try:
                query = "SELECT supplierID, name FROM suppliers"
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    suppliers.append((row["supplierID"], row["name"]))  # Return tuples

                return suppliers
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return []
