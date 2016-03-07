import os
import pymongo
from pymongo import MongoClient
import datetime
import time
import praw
import json

def treat_subreddit_submissions(subreddit_name, subreddit, mongoDB, old_timestamp, new_timestamp):
     submissions = subreddit.get_new(limit=None)
     subreddit_submissions_db = mongoDB[subreddit_name+"_submissions"]
     while True:
         submission = submissions.next()

         if submission.created_utc >= new_timestamp:
             continue

         if submission.created_utc < old_timestamp:
             break
         
         submission_db = {
             "submission_timestamp" : submission.created_utc,
             "submission_title" : submission.title
         }

         subreddit_submissions_db.insert_one(submission_db)    
         print "Added a new submission in subreddit "+subreddit_name     
         
def treat_subreddit_comments(subreddit_name, subreddit, mongoDB, old_timestamp, new_timestamp):
     comments = subreddit.get_comments(limit=None)
     subreddit_comments_db = mongoDB[subreddit_name+"_comments"]
     while True:
         comment = comments.next()

         # these comments will be processed in the next batch
         if comment.created_utc >= new_timestamp:
             continue

         if comment.created_utc < old_timestamp:
             break

         comment_db = {
             "comment_timestamp" : comment.created_utc,
             "comment_body" : comment.body
         }

         subreddit_comments_db.insert_one(comment_db)
         print "Added a new comment in subreddit "+subreddit_name

def treat_subreddit(subreddit_name, redditClient, mongoDB, old_timestamp, new_timestamp):
     subreddit = redditClient.get_subreddit(subreddit_name)
     treat_subreddit_submissions(subreddit_name, subreddit, mongoDB, old_timestamp, new_timestamp)
     treat_subreddit_comments(subreddit_name, subreddit, mongoDB, old_timestamp, new_timestamp)

def get_current_timestamp():
     current_date = datetime.datetime.utcnow()
     current_timestamp = (current_date - datetime.datetime(1970,1,1)).total_seconds()
     return current_timestamp

def create_indexes_for_subreddit(subreddit_name, mongoDB):
     subreddit_comments_db = mongoDB[subreddit_name+"_comments"]
     subreddit_submissions_db = mongoDB[subreddit_name+"_submissions"]
     subreddit_comments_db.create_index([
         ("comment_timestamp", pymongo.DESCENDING),
         ("comment_body", pymongo.TEXT)
     ], name="comment_search_index")
     subreddit_submissions_db.create_index([
         ("submission_timestamp", pymongo.DESCENDING),
         ("submission_title", pymongo.TEXT)
     ], name="submission_search_index")

def initialize_database(subreddits, mongoDB, mongoClient):
     mongoClient.admin.command("setParameter", textSearchEnabled=True)
     for subreddit in subreddits:
         create_indexes_for_subreddit(subreddit, mongoDB)

def loop(client):
     while True:
         db = client.test_database
         collection = db.test_collection
         post = {"date": datetime.datetime.utcnow()}
         collection.insert_one(post)
         time.sleep(5)


def run():
     file = open('subreddits.json', 'r')
     subreddits_json = file.read()
     subreddits = json.loads(subreddits_json)
     redditClient = praw.Reddit(user_agent="Test Script")     
     mongoClient = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
     mongoDB = mongoClient.challange
     initialize_database(subreddits, mongoDB, mongoClient)
     old_timestamp = get_current_timestamp()
     while True:
         time.sleep(30)
         print "Woke from sleep, starting to process subreddits"
         new_timestamp = get_current_timestamp()
         for subreddit in subreddits:
             treat_subreddit(subreddit.lower(), redditClient, mongoDB, old_timestamp, new_timestamp)
         old_timestamp = new_timestamp
         print "Processed all subreddits, going to sleep"

run()
