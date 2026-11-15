import db

def get_movies():
    sql = """SELECT m.id, m.title, m.release_year, u.id user_id, u.username
             FROM movies m, users u
             WHERE m.user_id = u.id
             ORDER BY m.id DESC"""
    return db.query(sql)

def get_movie(movie_id):
    sql = """SELECT m.id, m.title, m.description, m.release_year,
                    u.id user_id, u.username
             FROM movies m, users u
             WHERE m.user_id = u.id AND m.id = ?"""
    result = db.query(sql, [movie_id])
    return result[0] if result else None
