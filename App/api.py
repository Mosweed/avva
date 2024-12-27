from flask import Flask, redirect, url_for, request, render_template, jsonify
from app import app, mail
import mysql.connector
from mysql.connector import Error
from App.classes.products import Product
from App.classes.suppliers import Supplier
from flask_mail import Message
from flask import session
import random


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


@app.route("/api/products", methods=["POST", "GET"])
def ajaxfile():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if request.method == "POST":
            draw = request.form["draw"]
            row = int(request.form["start"])
            rowperpage = int(request.form["length"])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)

            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from products")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"]
            print(totalRecords)

            ## Total number of records with filtering
            likeString = "%" + searchValue + "%"
            cursor.execute(
                "SELECT count(*) as allcount from products WHERE name LIKE %s OR productID LIKE %s  ",
                (likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"]
            print(totalRecordwithFilter)

            ## Fetch records
            if searchValue == "":
                cursor.execute(
                    "SELECT * FROM products ORDER BY  productID   asc limit %s, %s ;",
                    (row, rowperpage),
                )
                employeelist = cursor.fetchall()
            else:
                cursor.execute(
                    "SELECT * FROM products  WHERE name LIKE %s OR productID LIKE %s  ORDER BY productID   limit %s, %s ;",
                    (likeString, likeString, row, rowperpage),
                )
                employeelist = cursor.fetchall()

            data = []
            for row in employeelist:
                data.append(
                    {
                        "productID": row["productID"],
                        "name": row["name"],
                        "article_number": row["article_number"],
                        "stock": row["stock"],
                        "minimum_stock": row["minimum_stock"],
                    }
                )

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


@app.route("/api/suppliers", methods=["POST", "GET"])
def ajaxfile_suppliers():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if request.method == "POST":
            draw = request.form["draw"]
            row = int(request.form["start"])
            rowperpage = int(request.form["length"])
            searchValue = request.form["search[value]"]

            # Total records without filtering
            cursor.execute("SELECT COUNT(*) as allcount FROM suppliers")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount["allcount"]

            # Total records with filtering
            likeString = "%" + searchValue + "%"
            cursor.execute(
                "SELECT COUNT(*) as allcount FROM suppliers WHERE name LIKE %s OR website LIKE %s OR supplierID LIKE %s ",
                (likeString, likeString, likeString),
            )
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount["allcount"]

            # Fetch records
            if searchValue == "":
                cursor.execute(
                    "SELECT * FROM suppliers ORDER BY name ASC LIMIT %s, %s;",
                    (row, rowperpage),
                )
                supplierlist = cursor.fetchall()
            else:
                cursor.execute(
                    "SELECT * FROM suppliers WHERE  name LIKE %s OR website LIKE %s OR supplierID LIKE %s LIMIT %s, %s;",
                    (likeString, likeString, likeString, row, rowperpage),
                )
                supplierlist = cursor.fetchall()

            # Prepare response data
            data = []
            for row in supplierlist:
                data.append(
                    {
                        "supplierID": row["supplierID"],
                        "name": row["name"],
                        "phone_number": row["phone_number"],
                        "street_name": row["street_name"],
                        "house_number": row["house_number"],
                        "postal_code": row["postal_code"],
                        "website": row["website"],
                    }
                )

            response = {
                "draw": draw,
                "iTotalRecords": totalRecords,
                "iTotalDisplayRecords": totalRecordwithFilter,
                "aaData": data,
            }

            return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
