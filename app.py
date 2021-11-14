import flask
import os
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

from dotenv import load_dotenv, find_dotenv
from flask_login import (
    login_user,
    UserNow,
    LoginManager,
    login_required,
)

load_dotenv(find_dotenv())

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(UserNow, db.Model):

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


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)