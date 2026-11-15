import csv
import os
import random
import sqlite3
import time

from werkzeug.security import generate_password_hash

USER_COUNT = 20
MOVIE_COUNT = 80
SEED_PASSWORD = "seed-password"
FILMS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "films.csv")

def load_films():
    with open(FILMS_PATH, encoding="utf-8", newline="") as file:
        return [(row["title"], int(row["year"]), row["genres"].split(";"))
                for row in csv.DictReader(file)]

def main():
    random.seed(1)
    films = load_films()
    started = time.time()

    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    existing = con.execute("SELECT COUNT(*) FROM users WHERE username = ?", ["user1"]).fetchone()[0]
    if existing:
        print("database already seeded; delete database.db and recreate it first")
        return

    password_hash = generate_password_hash(SEED_PASSWORD)
    user_ids = []
    for i in range(1, USER_COUNT + 1):
        cursor = con.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                             [f"user{i}", password_hash])
        user_ids.append(cursor.lastrowid)

    for _ in range(MOVIE_COUNT):
        title, year, genres = random.choice(films)
        user_id = random.choice(user_ids)
        cursor = con.execute(
            """INSERT INTO movies (title, description, release_year, user_id)
               VALUES (?, ?, ?, ?)""",
            [title, "Seed data for testing.", year, user_id])
        movie_id = cursor.lastrowid
        con.execute("INSERT INTO movie_classes (movie_id, title, value) VALUES (?, ?, ?)",
                    [movie_id, "Genre", random.choice(genres)])
        con.execute("INSERT INTO movie_classes (movie_id, title, value) VALUES (?, ?, ?)",
                    [movie_id, "Decade", f"{year // 10 * 10}s"])

    con.commit()
    con.close()
    print(f"seeded {USER_COUNT} users and {MOVIE_COUNT} movies in {time.time() - started:.1f} s")

if __name__ == "__main__":
    main()
