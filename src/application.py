import os
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if not os.getenv("GOODREADS_API_KEY"):
    raise RuntimeError("GOODREADS_API_KEY not set")

goodreads_key = os.getenv("GOODREADS_API_KEY")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    books_preview = ()
    for x in range(5):
        books_preview += (random.randint(1,5000),)
    books = db.execute("select * from books where book_id in :books_preview", {"books_preview": books_preview}).fetchall()
    try:
        user_id = session["user_id"]
        return render_template("index.html", books=books, logged_in=True)
    except KeyError:
        return render_template("index.html", books=books, logged_in=False) 
        

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/api/<int:isbn>", methods=["GET"])
def isbn_search(isbn):
    book = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html")
    