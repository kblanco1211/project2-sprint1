"""Main app file that contains flask server logic."""
import os
import flask
from flask import render_template,request,redirect
from flask_login import login_required, current_user, login_user
from opensea import get_assets, get_single_asset
from dotenv import load_dotenv, find_dotenv
from models import UserModel,db,login

load_dotenv(find_dotenv())

app = flask.Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


if os.getenv("DATABASE_URL") is not None:  # so our unit tests run in GitHub
    db.create_all()
login.login_view = "login"
login.init_app(app)

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
@login_required
def saved():
    """Route that displays a user's displayed NFTs."""

    return flask.render_template("saved.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/explore')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/explore')
     
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect('/explore')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/explore')
    return render_template('signup.html')


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


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
