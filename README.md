The challange
=============

Currently done task 4, with the Docker infrastructure with composer.

Proof of concept implementation:
The script container inserts data into the mongodb once every 5 seconds and the webserver returns the number of documents in the db.
The webserver forwords its web port to the hosts 80 port, to make testing easier - just curl localhost.

Used mongo and python docker images.
Docker version used : 1.7.1
Docker-compose version used : 1.5.2
