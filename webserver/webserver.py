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
         "submission_timestamp" : {"$gt" : from_timestamp-1, "$lt" : to_timestamp+1} 
     })
     cursor.sort([("submission_timestamp", pymongo.DESCENDING)])
     submissions = []
     for submission in cursor:
        submissions.append({
           "submission_timestamp" : submission["submission_timestamp"],
           "submission_title" : submission["submission_title"]
        })
     return submissions
     

def subreddit_get_submissions_keyword(subreddit_name, mongoDB, from_timestamp, to_timestamp, keyword):
     cursor = mongoDB[subreddit_name+"_submissions"].find({
         "$text":{"$search":keyword},
         "submission_timestamp" : {"$gt" : from_timestamp-1, "$lt" : to_timestamp+1}
     })
     cursor.sort([("submission_timestamp", pymongo.DESCENDING)])
     submissions = []
     for submission in cursor:
         submissions.append({
             "submission_timestamp" : submission["submission_timestamp"],
             "submission_title" : submission["submission_title"]
         })
     return submissions



def subreddit_get_comments(subreddit_name, mongoDB, from_timestamp, to_timestamp):
     cursor = mongoDB[subreddit_name+"_comments"].find({
         "comment_timestamp" : {"$gt" : from_timestamp-1, "$lt" : to_timestamp+1}
     })
     cursor.sort([("comment_timestamp", pymongo.DESCENDING)])
     comments = []
     for comment in cursor:
         comments.append({
             "comment_timestamp" : comment["comment_timestamp"],
             "comment_body" : comment["comment_body"]
         })
     return comments

     
def subreddit_get_comments_keyword(subreddit_name, mongoDB, from_timestamp, to_timestamp, keyword):
     cursor = mongoDB[subreddit_name+"_comments"].find({
         "$text":{"$search":keyword},
         "comment_timestamp" : {"$gt" : from_timestamp-1, "$lt" : to_timestamp+1}
     })
     cursor.sort([("comment_timestamp", pymongo.DESCENDING)])
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

     if (not args.has_key("keyword")):
         response = {
             "submissions" : subreddit_get_submissions(subreddit_name, mongoDB, from_timestamp, to_timestamp),
             "comments" : subreddit_get_comments(subreddit_name, mongoDB, from_timestamp, to_timestamp)
         }
     else:
         keyword = args.get("keyword")
         response = {
             "submissions" : subreddit_get_submissions_keyword(subreddit_name, mongoDB, from_timestamp, to_timestamp, keyword),
             "comments" : subreddit_get_comments_keyword(subreddit_name, mongoDB, from_timestamp, to_timestamp, keyword)
         }
     return json.dumps(response)

if not app.debug:
    import logging
    file_handler = logging.FileHandler("/var/log/flask.log")
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
