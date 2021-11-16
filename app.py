"""Main app file that contains flask server logic."""

import os
import flask
from flask_sqlalchemy import SQLAlchemy
from opensea import get_assets, get_single_asset

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)


@app.route("/")
def index():
    """App homepage"""

    return flask.render_template("index.html")


@app.route("/explore")
def explore():
    """Route for the explore NFTs page that allows users to pick an NFT to learn more about it and its details."""

    assets = get_assets()

    if assets == "error":
        return flask.render_template("api_error.html", error="explore")

    return flask.render_template(
        "explore.html",
        image_urls=assets["image_urls"],
        names=assets["names"],
        collections=assets["collections"],
        contract_addresses=assets["contract_addresses"],
        token_ids=assets["token_ids"],
    )


@app.route("/details", methods=["POST"])
def details():
    """Route that displays and explains the details of a chosen NFT."""

    contract_address = flask.request.form.get("contract_address")
    token_id = flask.request.form.get("token_id")
    asset_details = get_single_asset(contract_address, token_id)

    if asset_details == "error":
        return flask.render_template("api_error.html", error="details")

    return flask.render_template(
        "details.html",
        image_url=asset_details["image_url"],
        name=asset_details["name"],
        collection=asset_details["collection"],
        collection_description=asset_details["collection_description"],
        description=asset_details["description"],
        creator=asset_details["creator"],
        price=asset_details["price"],
        crypto=asset_details["crypto"],
        trait_types=asset_details["trait_types"],
        traits=asset_details["traits"],
        contract_address=contract_address,
        token_id=token_id,
    )


@app.route("/save_nft", methods=["POST"])
def save_nft():
    """Route that saves an NFT to a user's list of saved NFTs"""

    contract_address = flask.request.form.get("contract_address")
    token_id = flask.request.form.get("token_id")

    # add logic to add NFT to saved NFT table

    flask.flash("NFT has been successfully saved")

    asset_details = get_single_asset(contract_address, token_id)

    if asset_details == "error":
        return flask.render_template("api_error.html", error="details")

    return flask.render_template(
        "details.html",
        image_url=asset_details["image_url"],
        name=asset_details["name"],
        collection=asset_details["collection"],
        collection_description=asset_details["collection_description"],
        description=asset_details["description"],
        creator=asset_details["creator"],
        price=asset_details["price"],
        crypto=asset_details["crypto"],
        trait_types=asset_details["trait_types"],
        traits=asset_details["traits"],
        contract_address=contract_address,
        token_id=token_id,
    )


@app.route("/saved")
def saved():
    """Route that displays a user's displayed NFTs."""

    return flask.render_template("saved.html")


@app.route("/login")
def login():
    """Login page"""

    return flask.render_template("login.html")


@app.route("/signup")
def signup():
    """Sign up page"""

    return flask.render_template("signup.html")


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
