import mysql.connector
from mysql.connector import Error
from App import app  
from App.classes.db import db
from App.classes.suppliers import Supplier

class Product(db):
    def __init__(self, productID=None,  name=None, article_number=None,
                 stock=None, minimum_stock=None, perishable=None, adviceID=None,
                 energy_cost=None, packaging_size=None, storage_locationID=None, advice = None , storage_location = None ,suppliers=None):
        self.productID = productID
        self.name = name
        self.article_number = article_number
        self.stock = stock
        self.minimum_stock = minimum_stock
        self.perishable = perishable
        self.adviceID = adviceID
        self.energy_cost = energy_cost
        self.packaging_size = packaging_size
        self.storage_locationID = storage_locationID
        self.advice = advice
        self.storage_location = storage_location
        self.suppliers = []
   
    
    @staticmethod
    def get_by_id(productID):
        """ Fetch a product by its ID with related data """
        connection = Product.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                
                query = """
	SELECT p.* , sa.advice , sl.storage_name as storage_location   FROM products p  
inner join storage_locations sl on sl.storage_locationID = p.storage_locationID
inner join storage_advice sa on sa.adviceID = p.adviceID where
 p.productID = %s
                """
                cursor.execute(query, (productID,))
                row = cursor.fetchone()
                if row:
                   

                    return Product(
                        productID=row['productID'],
                        name=row['name'],
                        article_number=row['article_number'],
                        stock=row['stock'],
                        minimum_stock=row['minimum_stock'],
                        perishable=row['perishable'],
                        adviceID=row['adviceID'],
                        energy_cost=row['energy_cost'],
                        packaging_size=row['packaging_size'],
                        storage_locationID=row['storage_locationID'],
                        advice=row['advice'],
                        storage_location=row['storage_location']
                    )
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return None

    @staticmethod
    def get_all():
        """ Fetch all products with related data """
        connection = Product.create_connection()
        products = []
        cursor = connection.cursor(dictionary=True)

        if connection:
            try:
                query = """
                SELECT p.* , s.name as supplier , sa.advice , sl.storage_name as storage_location   FROM products p  inner join suppliers s
on p.supplierID = s.supplierID
inner join storage_locations sl on sl.storage_locationID = p.storage_locationID
inner join storage_advice sa on sa.adviceID = p.adviceID order by p.productID


                """
                cursor.execute(query)
                rows = cursor.fetchall()

                # Convert rows to Product objects with related data
                for row in rows:
                    

                    product = Product(
                        productID=row['productID'],
                        name=row['name'],
                        article_number=row['article_number'],
                        stock=row['stock'],
                        minimum_stock=row['minimum_stock'],
                        perishable=row['perishable'],
                        adviceID=row['adviceID'],
                        energy_cost=row['energy_cost'],
                        packaging_size=row['packaging_size'],
                        storage_locationID=row['storage_locationID'],
                        supplier=row['supplier'],
                        advice=row['advice'],
                        storage_location=row['storage_location']
                    )
                    products.append(product)

                return products
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return []
    def create(self):
        """ Create a new product in the database """
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    INSERT INTO products 
                    (supplierID, name, article_number, stock, minimum_stock, perishable,
                     adviceID, energy_cost, packaging_size, storage_locationID) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (self.name, self.article_number, self.stock,
                                       self.minimum_stock, self.perishable, self.adviceID,
                                       self.energy_cost, self.packaging_size, self.storage_locationID))
                connection.commit()
                self.productID = cursor.lastrowid
                print(f"Product created successfully with ID: {self.productID}")
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    def edit(self):
        """ Edit an existing product in the database """
        if not self.productID:
            print("Error: Cannot edit a product without a valid productID.")
            return

        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    UPDATE products 
                    SET supplierID = %s, name = %s, article_number = %s, stock = %s, 
                        minimum_stock = %s, perishable = %s, adviceID = %s, 
                        energy_cost = %s, packaging_size = %s, storage_locationID = %s
                    WHERE productID = %s
                """
                cursor.execute(query, ( self.name, self.article_number, self.stock,
                                       self.minimum_stock, self.perishable, self.adviceID,
                                       self.energy_cost, self.packaging_size, self.storage_locationID,
                                       self.productID))
                connection.commit()
                print(f"Product with ID {self.productID} updated successfully!")
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
                
                


    
    def get_suppliers(self):
        """ Fetch all suppliers for a product """
        
        print(self.productID)
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                query = """
                    SELECT s.* FROM suppliers_has_products sp inner join suppliers s on s.supplierID = sp.suppliers_supplierID 
                    where sp.products_productID  = %s
                """
                cursor.execute(query, (self.productID,))
                rows = cursor.fetchall()
                for row in rows:
                    supplier = Supplier(
                        supplierID=row['supplierID'],
                        name=row['name'],
                        phone_number=row['phone_number']
                    )
                    print(supplier)
                    self.suppliers.append(supplier)
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return self.suppliers
