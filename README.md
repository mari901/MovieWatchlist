# Movie Watchlist

A web application for keeping track of movies: users create an account, add movies to a shared database, and organize them by genre and decade. Users can edit and remove the movies they added, search the whole list, and leave a rating and comment on any movie.

## Features

* Users can create an account and log in to the application.
* Logged-in users can add, edit and delete their own movies.
* Users can see all movies added to the application, their own and other users'.
* Users can search movies by title or description.
* Each movie can have one or more genres and one decade, chosen from options stored in the database.
* Users can rate movies from 1 to 5 and leave a comment, which is shown on the movie page.
* User pages show how many movies a user has added, and list those movies.

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

Start the application:

```
$ flask run
```

Then open http://127.0.0.1:5000 in a browser.

## Testing

Register a user, log in, and add a movie. Log out and register a second user to check that the first user's movie can be seen but not edited or deleted. Try searching for part of a movie title, and try submitting forms with empty fields or titles longer than the allowed limit.
