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


# route for the explore NFTs page that allows users to pick an NFT to learn more about it and its details
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


# route that displays and explains the details of a chosen NFT
@app.route("/details")
def details():
    asset_details = get_single_asset()

    return flask.render_template("details.html")


# route that displays a user's displayed NFTs
@app.route("/saved")
def saved():
    return flask.render_template("saved.html")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
