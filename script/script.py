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

def treat_subreddit_submissions(subreddit_name, subreddit, time_limit):
     submissions = subreddit.get_new(limit=None)
     while True:
         submission = submissions.next()
         if submission.created_utc < time_limit:
             break
         
         print(subreddit_name)
         print(submission.title)
         print(submission.created_utc)
         
def treat_subreddit_comments(subreddit_name, subreddit, time_limit):
     comments = subreddit.get_comments(limit=None)
     while True:
         comment = comments.next()
         if comment.created_utc < time_limit:
             break

         print(subreddit_name)
         print(comment.body)
         print(comment.created_utc)

def treat_subreddit(subreddit_name, reddit, time_limit):
     subreddit = reddit.get_subreddit(subreddit_name)
     treat_subreddit_submissions(subreddit_name, subreddit, time_limit)
     treat_subreddit_comments(subreddit_name, subreddit, time_limit)

reddit = praw.Reddit(user_agent="Test Script")

current_date = datetime.datetime.utcnow()
current_timestamp = (current_date - datetime.datetime(1970,1,1)).total_seconds()

treat_subreddit("python".lower(), reddit, current_timestamp - 3600*24)

#run()
