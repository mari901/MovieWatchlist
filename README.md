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

Optional: fill the database with test data (20 users and 80 movies):

```
$ python seed.py
```

Run it only on a new database. The script refuses to run if the test users already exist. All seeded users have the password `seed-password`.

## Test data

`data/films.csv` lists 751 films from 1950 to 2024 with their release year and one or more genres. The titles, years and genres come from Wikidata, which publishes its data under the CC0 public-domain dedication. Only films with a genre matching one of the genres in `init.sql` are included. The genres are mapped from Wikidata's labels by keyword, so, for example, "stand-up comedy" becomes Comedy, and Comedy is the largest genre in the file.

`seed.py` gives each of its 80 movie rows a random film from this list, a random seeded user as its owner, one random genre, and the decade of the film's release year. Each movie description is the same placeholder text. Repeats are possible but unlikely with 80 movies. The random generator uses a fixed seed, so every run creates the same data.

Start the application:

```
$ flask run
```

Then open http://127.0.0.1:5000 in a browser.

## Testing

Register a user, log in, and add a movie with a genre and decade. Check that it appears on the front page and on its own page. Log out, register a second user, and check that the first user's movie can be seen but its edit and remove pages return an error. Search for part of the movie's title and for a word from its description, and search for something that does not exist.
