import unittest
import script

class TestScript(unittest.TestCase):

     class PrawStub():

         list = []

         def __init__(self, list):
             self.list = list

         def get_new(self, limit):
             return iter(self.list)

         def get_comments(self, limit):
             return iter(self.list)

     class MongoStub():
         
         list = []

         def __init__(self):
             self.list = []

         def insert_one(self, element):
             self.list.append(element)

     class Submission():
         
         created_utc = 0
         title = ""

         def __init__(self, created_utc, title):
             self.created_utc = created_utc
             self.title = title
     
     class Comment():

         created_utc = 0
         body = ""

         def __init__(self, created_utc, body):
             self.created_utc = created_utc
             self.body = body

     def test_submissions_empty(self):
         praw_subreddit = self.PrawStub([])
         mongo = self.MongoStub()
         script.treat_subreddit_submissions("test", praw_subreddit, {"test_submissions": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 0)

     def test_submissions_newer(self):
         praw_subreddit = self.PrawStub([self.Submission(11, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_submissions("test", praw_subreddit, {"test_submissions": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 0)

     def test_submissions_ok(self):
         praw_subreddit = self.PrawStub([self.Submission(8, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_submissions("test", praw_subreddit, {"test_submissions": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 1)

     def test_submissions_older(self):
         praw_subreddit = self.PrawStub([self.Submission(-1, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_submissions("test", praw_subreddit, {"test_submissions": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 0)

     def test_submissions_complex(self):
         praw_subreddit = self.PrawStub([self.Submission(11, "test"), self.Submission(9, "test"), self.Submission(0, "test"), self.Submission(-1, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_submissions("test", praw_subreddit, {"test_submissions": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 2)

     def test_comments_empty(self):
         praw_subreddit = self.PrawStub([])
         mongo = self.MongoStub()
         script.treat_subreddit_comments("test", praw_subreddit, {"test_comments": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 0)

     def test_comments_newer(self):
         praw_subreddit = self.PrawStub([self.Comment(11, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_comments("test", praw_subreddit, {"test_comments": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 0)

     def test_comments_ok(self):
         praw_subreddit = self.PrawStub([self.Comment(8, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_comments("test", praw_subreddit, {"test_comments": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 1)

     def test_comments_older(self):
         praw_subreddit = self.PrawStub([self.Comment(-1, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_comments("test", praw_subreddit, {"test_comments": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 0)

     def test_comments_complex(self):
         praw_subreddit = self.PrawStub([self.Comment(11, "test"), self.Comment(9, "test"), self.Comment(0, "test"), self.Comment(-1, "test")])
         mongo = self.MongoStub()
         script.treat_subreddit_comments("test", praw_subreddit, {"test_comments": mongo}, 0, 10)
         self.assertEqual(len(mongo.list), 2)

if __name__ == '__main__':
     unittest.main()
