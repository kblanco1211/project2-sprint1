import flask
import os
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/saved")
def saved():
    return flask.render_template("saved.html")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


app.run(host=os.getenv("IP", "127.0.0.1"), port=int(os.getenv("PORT", 8080)), debug=True)
