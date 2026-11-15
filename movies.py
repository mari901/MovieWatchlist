import db

MAX_ID = 2**63 - 1

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_movies():
    sql = """SELECT m.id, m.title, m.release_year, u.id user_id, u.username,
                    GROUP_CONCAT(c.value, ', ') genres
             FROM movies m JOIN users u ON m.user_id = u.id
                           LEFT JOIN movie_classes c
                           ON c.movie_id = m.id AND c.title = 'Genre'
             GROUP BY m.id
             ORDER BY m.id DESC"""
    return db.query(sql)

def get_movie(movie_id):
    if movie_id > MAX_ID:
        return None
    sql = """SELECT m.id, m.title, m.description, m.release_year,
                    u.id user_id, u.username
             FROM movies m, users u
             WHERE m.user_id = u.id AND m.id = ?"""
    result = db.query(sql, [movie_id])
    return result[0] if result else None

def get_classes(movie_id):
    sql = "SELECT title, value FROM movie_classes WHERE movie_id = ? ORDER BY id"
    return db.query(sql, [movie_id])

def add_movie(title, description, release_year, user_id, classes):
    sql = """INSERT INTO movies (title, description, release_year, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, release_year, user_id])

    movie_id = db.last_insert_id()

    sql = "INSERT INTO movie_classes (movie_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [movie_id, class_title, class_value])

    return movie_id

def update_movie(movie_id, title, description, release_year, classes):
    sql = """UPDATE movies SET title = ?,
                               description = ?,
                               release_year = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, release_year, movie_id])

    sql = "DELETE FROM movie_classes WHERE movie_id = ?"
    db.execute(sql, [movie_id])

    sql = "INSERT INTO movie_classes (movie_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [movie_id, class_title, class_value])

def remove_movie(movie_id):
    sql = "DELETE FROM movie_classes WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movies WHERE id = ?"
    db.execute(sql, [movie_id])

def find_movies(query):
    sql = """SELECT m.id, m.title, m.release_year, u.id user_id, u.username
             FROM movies m, users u
             WHERE m.user_id = u.id AND
                   (m.title LIKE ? OR m.description LIKE ?)
             ORDER BY m.id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
