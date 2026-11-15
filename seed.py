import sqlite3

from werkzeug.security import generate_password_hash

SEED_USER = "seed"

MOVIES = [
    ("Singin' in the Rain", "A silent-film star learns to adapt when talkies arrive.", 1952,
     [("Genre", "Comedy"), ("Decade", "1950s")]),
    ("Rear Window", "A photographer confined to his flat suspects a neighbour of murder.", 1954,
     [("Genre", "Thriller"), ("Decade", "1950s")]),
    ("12 Angry Men", "A jury deliberates over a murder trial and one juror doubts the verdict.", 1957,
     [("Genre", "Drama"), ("Decade", "1950s")]),
    ("Psycho", "A woman on the run checks into a remote motel run by a disturbed man.", 1960,
     [("Genre", "Horror"), ("Decade", "1960s")]),
    ("2001: A Space Odyssey", "A mission to Jupiter goes wrong after an ancient monolith is found.", 1968,
     [("Genre", "Science fiction"), ("Decade", "1960s")]),
    ("The Good, the Bad and the Ugly", "Three gunmen race to find a hidden cache of gold during the Civil War.", 1966,
     [("Genre", "Action"), ("Decade", "1960s")]),
    ("The Godfather", "The aging head of a crime family hands control to his reluctant son.", 1972,
     [("Genre", "Drama"), ("Decade", "1970s")]),
    ("Jaws", "A police chief tries to close a beach hunted by a great white shark.", 1975,
     [("Genre", "Thriller"), ("Decade", "1970s")]),
    ("Star Wars", "A farm boy joins a rebel plot to destroy an imperial space station.", 1977,
     [("Genre", "Science fiction"), ("Decade", "1970s")]),
    ("Raiders of the Lost Ark", "An archaeologist races Nazi agents for a biblical relic.", 1981,
     [("Genre", "Action"), ("Decade", "1980s")]),
    ("The Terminator", "A soldier from the future travels back to protect a woman from a cyborg.", 1984,
     [("Genre", "Science fiction"), ("Decade", "1980s")]),
    ("Back to the Future", "A teenager travels back to 1955 and must fix his parents' meeting.", 1985,
     [("Genre", "Comedy"), ("Genre", "Science fiction"), ("Decade", "1980s")]),
    ("Jurassic Park", "A theme park of cloned dinosaurs turns deadly.", 1993,
     [("Genre", "Science fiction"), ("Decade", "1990s")]),
    ("The Shawshank Redemption", "A banker sentenced for murder forms a lasting friendship in prison.", 1994,
     [("Genre", "Drama"), ("Decade", "1990s")]),
    ("Pulp Fiction", "Interlocking stories of crime and redemption in Los Angeles.", 1994,
     [("Genre", "Thriller"), ("Decade", "1990s")]),
    ("Spirited Away", "A girl works in a spirit bathhouse to free her parents.", 2001,
     [("Genre", "Drama"), ("Decade", "2000s")]),
    ("Pan's Labyrinth", "A girl in post-war Spain finds a fairy tale that may be real.", 2006,
     [("Genre", "Horror"), ("Decade", "2000s")]),
    ("The Dark Knight", "Batman faces the Joker, who plunges Gotham into chaos.", 2008,
     [("Genre", "Action"), ("Decade", "2000s")]),
    ("Inception", "A thief who steals secrets from dreams is offered a chance at redemption.", 2010,
     [("Genre", "Science fiction"), ("Genre", "Thriller"), ("Decade", "2010s")]),
    ("Mad Max: Fury Road", "A drifter and a rebel escape a tyrant across the desert.", 2015,
     [("Genre", "Action"), ("Decade", "2010s")]),
    ("Parasite", "A poor family slowly infiltrates the household of a wealthy one.", 2019,
     [("Genre", "Thriller"), ("Genre", "Drama"), ("Decade", "2010s")]),
    ("Everything Everywhere All at Once", "A laundromat owner jumps between parallel universes.", 2022,
     [("Genre", "Comedy"), ("Genre", "Science fiction"), ("Decade", "2020s")]),
    ("Oppenheimer", "The story of the physicist who led the development of the atomic bomb.", 2023,
     [("Genre", "Drama"), ("Decade", "2020s")]),
    ("Dune: Part Two", "Paul Atreides unites with the Fremen to take revenge on his enemies.", 2024,
     [("Genre", "Science fiction"), ("Decade", "2020s")]),
]

def get_seed_user_id(con):
    row = con.execute("SELECT id FROM users WHERE username = ?", [SEED_USER]).fetchone()
    if row:
        return row[0]
    password_hash = generate_password_hash(SEED_USER)
    cursor = con.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                         [SEED_USER, password_hash])
    return cursor.lastrowid

def main():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    user_id = get_seed_user_id(con)

    added = 0
    for title, description, release_year, classes in MOVIES:
        exists = con.execute("SELECT id FROM movies WHERE title = ?", [title]).fetchone()
        if exists:
            continue
        cursor = con.execute(
            """INSERT INTO movies (title, description, release_year, user_id)
               VALUES (?, ?, ?, ?)""",
            [title, description, release_year, user_id])
        movie_id = cursor.lastrowid
        for class_title, class_value in classes:
            con.execute("INSERT INTO movie_classes (movie_id, title, value) VALUES (?, ?, ?)",
                        [movie_id, class_title, class_value])
        added += 1

    con.commit()
    con.close()
    print(f"added {added} movies")

if __name__ == "__main__":
    main()
