import unittest
import webserver

class TestWebserver(unittest.TestCase):

     class CursorStub():

         list = []

         def __init__(self, list):
             self.list = list

         def sort(self, params):
             self.list = self.list

         def __iter__(self):
             return iter(self.list)

     class MongoStub():
         
         list = []

         def __init__(self, list):
             self.list = list

         def find(self, params):
             return TestWebserver.CursorStub(self.list)


     def test_submissions_get(self):
         mongo = self.MongoStub([{"submission_timestamp":0,"submission_title":"test"}])
         results = webserver.subreddit_get_submissions("test", {"test_submissions":mongo}, 0, 10)
         self.assertEqual(len(results), 1)         


     def test_submissions_get_keyword(self):
         mongo = self.MongoStub([{"submission_timestamp":0,"submission_title":"test"}])
         results = webserver.subreddit_get_submissions_keyword("test", {"test_submissions":mongo}, 0, 10, "test")
         self.assertEqual(len(results), 1)

     def test_comments_get(self):
         mongo = self.MongoStub([{"comment_timestamp":0,"comment_body":"test"}])
         results = webserver.subreddit_get_comments("test", {"test_comments":mongo}, 0, 10)
         self.assertEqual(len(results), 1)


     def test_comments_get_keyword(self):
         mongo = self.MongoStub([{"comment_timestamp":0,"comment_body":"test"}])
         results = webserver.subreddit_get_comments_keyword("test", {"test_comments":mongo}, 0, 10, "test")
         self.assertEqual(len(results), 1)


if __name__ == '__main__':
     unittest.main()
