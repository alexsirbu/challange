import json
import os
import pymongo
from pymongo import MongoClient
import datetime
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
     client = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
     db = client.test_database
     collection = db.test_collection	
     return json.dumps(collection.count())

if __name__ == "__main__":
    app.run(host='0.0.0.0')
