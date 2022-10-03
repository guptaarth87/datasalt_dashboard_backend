from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.secret_key="secretkey"
mongo_uri="mongodb+srv://arthgupta861:arthgupta861@cluster0.1mixk.mongodb.net/data_salt?retryWrites=true&w=majority"
app.config["MONGO_URI"]=mongo_uri
mongo = PyMongo(app)