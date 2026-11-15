# Movie Watchlist

A web application for keeping track of movies. Users create an account, add movies to a shared list, and organize them by genre and decade. Users can edit and remove the movies they added, and search the whole list by title or description.

## Features

* Users can create an account and log in to the application.
* Logged-in users can add, edit and delete their own movies.
* Users can see all movies added to the application, their own and other users'.
* Users can search movies by title or description.
* Each movie can have one or more genres and one decade, chosen from options stored in the database.

Planned for later: rating and commenting on movies, and user pages with statistics.

## Installation

Install the `flask` library:

```
$ pip install flask
```

Create the database tables and add the genre and decade options:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Optional: add a sample set of 24 films, three from each decade:

```
$ python seed.py
```

Start the application:

```
$ flask run
```

Then open http://127.0.0.1:5000 in a browser.

## Testing

Register a user, log in, and add a movie with a genre and decade. Check that it appears on the front page and on its own page. Log out, register a second user, and check that the first user's movie can be seen but its edit and remove pages return an error. Search for part of the movie's title and for a word from its description, and search for something that does not exist.
