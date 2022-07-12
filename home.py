from flask import Flask
from flask import Blueprint

# use url/home/hello to run functionality
home_bp = Blueprint('home', __name__)

@home_bp.route('/hello/')
def hello():
    return "Hello from Home Page"