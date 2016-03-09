The challange
=============

Implemented all the tasks.

To run: docker-compose up -d and then do curls into localhost (set up port 80 to be linked to webserver port).

Task 1 - implemented script which queries Reddit on given subreddits in the .json file provided and saves to MongoDB, then the webserver returns info from the db as required. Used collections based on reddit name and type of object which is searched (could have made a single db for each subreddit and group submissions and comments as an item, as they both have content and timestamp, but decided to have them separated, in order to allow the addition of new elements and searches).

Task 2 - added indexes to the db (first text on content, then on the timestamp) and implemented the text search in the content.

Task 3 - performed tests for both components, using stubs for the Reddit and Mongo clients. For the script, tested the Reddit querying, and for the webserver checked if all the functions run as expected (return what the db return). To run tests, run python script/webserver_tests.py.

Task 4 - used docker for running the machines and did a compose file, to start everything that was needed.

The coding style isn't the best, as I haven't worked in python in an production environment.
