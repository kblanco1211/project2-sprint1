"""Main app file that contains flask server logic."""

import os
import flask
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login.utils import login_required

from opensea import get_assets, get_single_asset

app = flask.Flask(__name__)

from dotenv import load_dotenv, find_dotenv
from flask_login import (
    login_user,
    UserMixin,
    LoginManager,
    login_required,
)

load_dotenv(find_dotenv())

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

# db.create_all()
# login_manager = LoginManager()
# login_manager.login_view = "login"
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_name):
#     return User.query.get(user_name)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        """
        Getter for username attribute
        """
        return self.username


print("Hello")

db.create_all()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    """
    Needed for login
    """
    return User.query.get(user_name)


@login_required
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


@app.route("/login", methods=["POST"])
def login_post():
    """
    Handler for login form data
    """
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("bp.index"))

    return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


@app.route("/save", methods=["POST"])
@app.route("/signup")
def signup():
    """Sign up page"""

    return flask.render_template("signup.html")


@app.route("/why")
def why():
    return flask.render_template("why.html")


@app.route("/history")
def history():
    return flask.render_template("history.html")


@app.route("/crypto")
def crypto():
    return flask.render_template("crypto.html")


@app.route("/purchase")
def purchase():
    return flask.render_template("purchase.html")


@app.route("/future")
def future():
    return flask.render_template("future.html")

@app.route("/wallets")
def wallets():
    return flask.render_template("wallets.html")

@app.route("/ethereum")
def ethereum():
    return flask.render_template("ethereum.html")

@app.route("/polygon")
def polygon():
    return flask.render_template("polygon.html")

@app.route("/klaytn")
def klaytn():
    return flask.render_template("klaytn.html")





app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
