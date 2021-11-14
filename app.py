import flask
import os
from flask_sqlalchemy import SQLAlchemy
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

db = SQLAlchemy(app)


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


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
