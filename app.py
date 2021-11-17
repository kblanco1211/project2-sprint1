"""Main app file that contains flask server logic."""
import os
import flask
<<<<<<< HEAD
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin
from opensea import get_assets, get_single_asset
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
class NFTsave(db.Model):
    __tablename__= 'nfts'
    id = db.Column(db.Integer, primary_key=True)
    contract_address = db.Column(db.String(200), nullable=False)
    token_id = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100))

db.create_all()

@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))    


@app.route("/")
@login_required
def index():
    """App homepage"""
    print("In index")

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
def details():
    """Route that displays and explains the details of a chosen NFT."""
    print("1")
    contract_address = flask.request.form.get("contract_address")
    token_id = flask.request.form.get("token_id")
    asset_details = get_single_asset(contract_address, token_id)
    print("2")
    if asset_details == "error":
        return flask.render_template("api_error.html", error="details")
    print("3")
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

    username = current_user.username
    NFT = NFTsave(
        contract_address=contract_address, token_id=token_id, username=username
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
    savednfts = NFTsave.query.filter_by(username = current_user.username).all()
    print(savednfts)
    return flask.render_template("saved.html", savednfts=savednfts)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            return redirect('/')
        if user == None:
            flask.flash("Invalid email or password, please try again.")
            return redirect("/login")

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return "Email already Present"

        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("signup.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


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


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
