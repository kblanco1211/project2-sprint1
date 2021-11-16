import flask
import os
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login.utils import login_required


app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# db.create_all()
# login_manager = LoginManager()
# login_manager.login_view = "login"
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_name):
#     return User.query.get(user_name)


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


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
