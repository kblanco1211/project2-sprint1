# implement main app/flask logic here
from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def signup():
    return render_template('login.html')


@app.route('/signup')
def login():
    return render_template('signup.html')



if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "127.0.0.1"),
        port=int(os.getenv('PORT', 8080)),
        debug=True,
    )