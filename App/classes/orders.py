from App import app
from App.classes.db import db


class Orders(db):
    # this class is used to interact with the orders table in the database the orders table has the following columns 
    # orderID, customerID, date , delivery_time , status , discount ,tracking_code , urgent ,  delivery_city , delivery_postcode  ,  delivery_house_number.
    
    def __init__(self, orderID=None, customerID=None, date=None, delivery_time=None, status=None, discount=None, tracking_code=None, urgent=None, delivery_city=None, delivery_postcode=None, delivery_house_number=None):
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
         
    