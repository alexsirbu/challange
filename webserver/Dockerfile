FROM python
ENV PYTHON_VERSION 2.7.11
RUN pip install Flask
RUN pip install pymongo
ADD webserver.py .
EXPOSE 5000
CMD [ "python", "./webserver.py" ]
