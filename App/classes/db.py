from app import app
import mysql.connector
from mysql.connector import Error


class db:

    @staticmethod
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
