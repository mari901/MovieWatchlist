import re
import secrets

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session

import config
import movies
import users

app = Flask(__name__)
app.secret_key = config.secret_key

MULTI_VALUE_CLASSES = ["Genre"]

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def parse_classes(entries):
    all_classes = movies.get_all_classes()
    classes = []
    for entry in entries:
        if entry:
            parts = entry.split(":")
            if len(parts) != 2:
                abort(403)
            class_title, class_value = parts
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            if (class_title, class_value) in classes:
                abort(403)
            used_titles = [title for title, value in classes]
            if class_title in used_titles and class_title not in MULTI_VALUE_CLASSES:
                abort(403)
            classes.append((class_title, class_value))
    return classes

def check_movie_fields(title, description, release_year):
    if not title.strip() or len(title) > 100:
        abort(403)
    if not description.strip() or len(description) > 1000:
        abort(403)
    if not re.search("^[0-9]{4}$", release_year):
        abort(403)
    if not 1888 <= int(release_year) <= 2100:
        abort(403)

@app.route("/")
def index():
    all_movies = movies.get_movies()
    return render_template("index.html", movies=all_movies)

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = movies.find_movies(query)
    else:
        query = ""
        results = []
    return render_template("search.html", query=query, results=results)

@app.route("/movie/<int:movie_id>")
def show_movie(movie_id):
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    classes = movies.get_classes(movie_id)
    return render_template("show_movie.html", movie=movie, classes=classes)

@app.route("/new_movie")
def new_movie():
    require_login()
    all_classes = movies.get_all_classes()
    return render_template("new_movie.html", all_classes=all_classes,
                           multi_value_classes=MULTI_VALUE_CLASSES)

@app.route("/create_movie", methods=["POST"])
def create_movie():
    require_login()
    check_csrf()

    title = request.form["title"]
    description = request.form["description"]
    release_year = request.form["release_year"]
    check_movie_fields(title, description, release_year)
    classes = parse_classes(request.form.getlist("classes"))

    movie_id = movies.add_movie(title, description, int(release_year),
                                session["user_id"], classes)
    flash("Movie added")
    return redirect("/movie/" + str(movie_id))

@app.route("/edit_movie/<int:movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    all_classes = movies.get_all_classes()

    if request.method == "GET":
        selected = set()
        for entry in movies.get_classes(movie_id):
            selected.add(entry["title"] + ":" + entry["value"])
        return render_template("edit_movie.html", movie=movie,
                               all_classes=all_classes, selected=selected,
                               multi_value_classes=MULTI_VALUE_CLASSES)

    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        description = request.form["description"]
        release_year = request.form["release_year"]
        check_movie_fields(title, description, release_year)
        classes = parse_classes(request.form.getlist("classes"))

        movies.update_movie(movie_id, title, description, int(release_year), classes)
        flash("Movie updated")
        return redirect("/movie/" + str(movie_id))

@app.route("/remove_movie/<int:movie_id>", methods=["GET", "POST"])
def remove_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_movie.html", movie=movie)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            movies.remove_movie(movie_id)
            flash("Movie removed")
            return redirect("/")
        return redirect("/movie/" + str(movie_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html", filled={})

    username = request.form["username"]
    if not username or len(username) > 16:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if len(password1) < 8 or len(password1) > 100:
        abort(403)

    if username != username.strip():
        flash("ERROR: The username cannot start or end with a space")
        return render_template("register.html", filled={"username": username})

    if password1 != password2:
        flash("ERROR: The passwords do not match")
        return render_template("register.html", filled={"username": username})

    if users.create_user(username, password1):
        flash("Account created, you can now log in")
        return redirect("/")

    flash("ERROR: That username is already taken")
    return render_template("register.html", filled={"username": username})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    flash("ERROR: Wrong username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    return redirect("/")
