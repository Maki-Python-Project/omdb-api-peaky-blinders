The goal of this exercise is to test if you know your way around developing
REST APIs in Python using docker. You can use any rest framework and database
of your choice. Approach it the way you would an actual long-term project.

To start with, a Dockerfile (with Python3.7 Alpine image) has been provided for you.
A docker-compose file with stubs for a sample SQL and a NoSQL database has also been provided.
Feel free to change it as per your choice of database.


## Tasks

Your task is to build a JSON-based REST API for your frontend developers to
consume. You have built a list of user stories with your colleagues, but you get
to decide how to design the API.

Required:

* Ability to import all episodes of all seasons of `Game of Thrones` from [OMDb API](http://www.omdbapi.com/).
(You will have to get an APIKey from http://www.omdbapi.com/apikey.aspx to use their API)
The APIs that should probably be used are in the following format:
http://www.omdbapi.com/?t=Game%20of%20Thrones&Season=1&apikey=<api key>
http://www.omdbapi.com/?i=<episode title id>&apikey=<api key> (for an episode)
* Design the data model to store this data. You need not store all the attributes of an episode.
Select the ones you think are important.
* Create GET API endpoints that can return episode information in a list format, as well as information for a specific episode, when retrieved by id
* Add filtering episodes by query params
* Design a data model to store basic text comments to be associated with a specific episode, along with a GET API to retrieve all of the comments for an episode
* Design and implement a separate CRUD API for these text comments.
* Ability to filter episodes where `imdbRating` is greater than 8.8 for a season or for all seasons.
* Add Users' permissions and authentication
* Add logging
* Update start.sh script to check if db is up
* Deploy your project to heroku

Nice to have:
* Download episodes data using celery
* Add caching
* Add pagination for episodes and comments
* Create custom manage.py command to retrieve episodes from omdb
* Write some tests
* Deploy your project to Amazon VPS instead of heroku
* Add ci/cd to your project