from flask import Flask

app = Flask(__name__)
from App import routes
from App import api
