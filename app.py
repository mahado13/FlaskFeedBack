from crypt import methods
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
# from forms import 

"""
Author: Mahad Osman
Date: Feb 7, 2023
Assginment: Flask Feedback
"""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """The homepage of our application"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """Registering a new user"""
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Logging a new user"""
    return render_template('login.html')


@app.route('/secret', methods=['GET'])
def secret():
    """Our secret page that only logged in users can view"""
    return render_template('secret.html')

