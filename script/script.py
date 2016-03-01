import os
import pymongo
from pymongo import MongoClient
import datetime
import time

def loop(client):
     while True:
         db = client.test_database
         collection = db.test_collection
         post = {"date": datetime.datetime.utcnow()}
         collection.insert_one(post)
         time.sleep(5)

def run():
     client = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
     loop(client)

run()
