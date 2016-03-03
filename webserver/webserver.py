import json
import os
import pymongo
from pymongo import MongoClient
import datetime
from flask import Flask
from flask import request
app = Flask(__name__)

def subreddit_get_submissions(subreddit_name, mongoDB, from_timestamp, to_timestamp):
     cursor = mongoDB[subreddit_name+"_submissions"].find({
         "submission_timestamp" : {"$gt" : from_timestamp-1}, 
         "submission_timestamp" : {"$lt" : to_timestamp+1}
     })
     submissions = []
     for submission in cursor:
        submissions.append({
           "submission_timestamp" : submission["submission_timestamp"],
           "submission_title" : submission["submission_title"]
        })
     return submissions
     

def subreddit_get_comments(subreddit_name, mongoDB, from_timestamp, to_timestamp):
     cursor = mongoDB[subreddit_name+"_comments"].find({
         "comment_timestamp" : {"$gt" : from_timestamp-1},
         "comment_timestamp" : {"$lt" : to_timestamp+1}
     })
     comments = []
     for comment in cursor:
         comments.append({
             "comment_timestamp" : comment["comment_timestamp"],
             "comment_body" : comment["comment_body"]
         })
     return comments
     

@app.route("/items/")
def hello():
     args = request.args
     if (not args.has_key("subreddit")) or (not args.has_key("from")) or (not args.has_key("to")):
        return json.dumps("Error: The request needs to have the subreddit, from and to keys")

     subreddit_name = args.get("subreddit")
     from_timestamp = args.get("from", type=int)
     to_timestamp = args.get("to", type=int)

     mongoClient = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
     mongoDB = mongoClient.challange
     response = {
         "submissions" : subreddit_get_submissions(subreddit_name, mongoDB, from_timestamp, to_timestamp),
         "comments" : subreddit_get_comments(subreddit_name, mongoDB, from_timestamp, to_timestamp)
     }
     return json.dumps(response)

if not app.debug:
    import logging
    file_handler = logging.FileHandler("/var/log/flask.log")
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
