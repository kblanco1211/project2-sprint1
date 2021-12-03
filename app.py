"""Main app file that contains flask server logic."""
import os
import flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_required,
    current_user,
    login_user,
    logout_user,
    LoginManager,
    UserMixin,
)
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from opensea import get_assets, get_single_asset

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class UserModel(UserMixin, db.Model):
    """Makes database to save user login"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        """generates hash for password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """checks password hash"""
        return check_password_hash(self.password_hash, password)


class NFTsave(db.Model):
    """Makes database to save user NFTs"""

    __tablename__ = "nfts"
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    contract_address = db.Column(db.String(200), nullable=False)
    token_id = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100))


db.create_all()


@login_manager.user_loader
def load_user(id):
    """loads user"""
    return UserModel.query.get(int(id))


@app.route("/")
@login_required
def index():
    """App homepage"""

    return flask.render_template("index.html")


@app.route("/explore")
@login_required
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
@login_required
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
        usd_price=asset_details["usd_price"],
        crypto="ETH",
        trait_types=asset_details["trait_types"],
        traits=asset_details["traits"],
        contract_address=contract_address,
        token_id=token_id,
    )


@app.route("/save_nft", methods=["POST"])
@login_required
def save_nft():
    """Route that saves an NFT to a user's list of saved NFTs"""

    image_url = flask.request.form.get("image_url")
    name = flask.request.form.get("name")
    contract_address = flask.request.form.get("contract_address")
    token_id = flask.request.form.get("token_id")

    username = current_user.username
    NFT = NFTsave(
        image_url=image_url,
        name=name,
        contract_address=contract_address,
        token_id=token_id,
        username=username,
    )
    db.session.add(NFT)
    db.session.commit()

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
@login_required
def saved():
    """Route that displays a user's displayed NFTs."""
    savednfts = NFTsave.query.filter_by(username=current_user.username).all()

    return flask.render_template("saved.html", savednfts=savednfts)


@app.route("/login", methods=["POST", "GET"])
def login():
    """Routes user to login"""
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form["email"]
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            return redirect("/")
        if user is None:
            flask.flash("Invalid email or password, please try again.")
            return redirect("/login")

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Routes user to sign up page"""
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        if UserModel.query.filter_by(email=email).first():
            return "Email already Present"

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("signup.html")


@app.route("/logout")
def logout():
    """logouts user"""
    logout_user()
    return redirect("/login")


@app.route("/why")
@login_required
def why():
    """routes to why tab"""
    return flask.render_template("why.html")


@app.route("/history")
@login_required
def history():
    """routes to history tab"""
    return flask.render_template("history.html")


@app.route("/crypto")
@login_required
def crypto():
    """routes to cryto tab"""
    return flask.render_template("crypto.html")


@app.route("/purchase")
@login_required
def purchase():
    """routes to purchase tab"""
    return flask.render_template("purchase.html")


@app.route("/future")
@login_required
def future():
    """routes to future tab"""
    return flask.render_template("future.html")


wallet2 = [
    "Metamask",
    "Coinbase Wallet",
    "Enjin",
    "Trust Wallet",
    "AlphaWallet",
    "Ledger",
]

images2 = [
    "/static/metamask.png",
    "/static/coinbase.png",
    "/static/enjin.png",
    "/static/trust.png",
    "/static/alpha.png",
    "/static/ledger.png",
]


@app.route("/wallets")
@login_required
def wallets():
    """routes to wallets tab"""
    return flask.render_template(
        "wallets.html",
        length=len(wallet2),
        wallets=wallet2,
        images=images2,
    )


@app.route("/ethereum")
@login_required
def ethereum():
    """routes to ethereum tab"""
    return flask.render_template("ethereum.html")


@app.route("/polygon")
@login_required
def polygon():
    """routes to polygon tab"""
    return flask.render_template("polygon.html")


@app.route("/klaytn")
@login_required
def klaytn():
    """routes to klaytn tab"""
    return flask.render_template("klaytn.html")


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
