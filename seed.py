from models import db, connect_db
from app import app


"""
Author: Mahad Osman
Date: Feb 7, 2023
Assginment: Flask Feedback
"""

#Create all tables 
db.drop_all()
db.create_all()

