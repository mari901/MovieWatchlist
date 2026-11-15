import secrets

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session

import config
import movies
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_movies = movies.get_movies()
    return render_template("index.html", movies=all_movies)

@app.route("/movie/<int:movie_id>")
def show_movie(movie_id):
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    return render_template("show_movie.html", movie=movie)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    username = request.form["username"]
    if not username or len(username) > 16:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not password1:
        abort(403)

    if password1 != password2:
        flash("VIRHE: Antamasi salasanat eivät ole samat")
        return render_template("register.html", filled={"username": username})

    if users.create_user(username, password1):
        flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
        return redirect("/")

    flash("VIRHE: Valitsemasi tunnus on jo varattu")
    return render_template("register.html", filled={"username": username})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer or "/")

    username = request.form["username"]
    password = request.form["password"]
    next_page = request.form["next_page"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect(next_page)

    flash("VIRHE: Väärä tunnus tai salasana")
    return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    return redirect("/")
