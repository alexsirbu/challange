FROM python:2.7
RUN pip install pymongo
RUN pip install praw
ADD script.py .
ADD subreddits.json .
CMD [ "python2", "./script.py" ]
