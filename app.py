import flask
import os
from flask_sqlalchemy import SQLAlchemy
from opensea import get_assets, get_single_asset

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/explore")
def explore():
    assets = get_assets()

    return flask.render_template(
        "explore.html",
        image_urls=assets["image_urls"],
        names=assets["names"],
        collections=assets["collections"],
        contract_addresses=assets["contract_addresses"],
        token_ids=assets["token_ids"],
    )


@app.route("/saved")
def saved():
    return flask.render_template("saved.html")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


app.run(debug=True)
