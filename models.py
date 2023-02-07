from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

"""
Author: Mahad Osman
Date: Feb 7, 2023
Assginment: Flask Feedback
"""
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """connects to our database"""
    db.app = app
    db.init_app(app)
