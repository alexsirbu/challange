FROM python:2.7
RUN pip install Flask
RUN pip install pymongo
ADD webserver.py .
ADD webserver_test.py .
EXPOSE 5000
CMD [ "python", "./webserver.py" ]
