import os
import pymongo
from pymongo import MongoClient
import datetime
import time
import praw

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

def treat_subreddit_submissions(subreddit_name, subreddit, mongoDB, time_limit):
     submissions = subreddit.get_new(limit=None)
     subreddit_submissions_db = mongoDB[subreddit_name+"_submissions"]
     while True:
         submission = submissions.next()
         if submission.created_utc < time_limit:
             break
         
         submission_db = {
             "submission_timestamp" : submission.created_utc,
             "submission_title" : submission.title
         }

         subreddit_submissions_db.insert_one(submission_db)         
         
def treat_subreddit_comments(subreddit_name, subreddit, mongoDB, time_limit):
     comments = subreddit.get_comments(limit=None)
     subreddit_comments_db = mongoDB[subreddit_name+"_comments"]
     while True:
         comment = comments.next()
         if comment.created_utc < time_limit:
             break

         comment_db = {
             "comment_timestamp" : comment.created_utc,
             "comment_body" : comment.body
         }

         subreddit_comments_db.insert_one(comment_db)

def treat_subreddit(subreddit_name, redditClient, mongoDB, time_limit):
     subreddit = redditClient.get_subreddit(subreddit_name)
     treat_subreddit_submissions(subreddit_name, subreddit, mongoDB, time_limit)
     treat_subreddit_comments(subreddit_name, subreddit, mongoDB, time_limit)

redditClient = praw.Reddit(user_agent="Test Script")
current_date = datetime.datetime.utcnow()
current_timestamp = (current_date - datetime.datetime(1970,1,1)).total_seconds()
mongoClient = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
mongoDB = mongoClient.challange
treat_subreddit("python".lower(), redditClient, mongoDB, current_timestamp - 3600*24)

#run()
