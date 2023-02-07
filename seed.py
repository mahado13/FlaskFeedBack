from models import db, connect_db, User
from app import app


"""
Author: Mahad Osman
Date: Feb 7, 2023
Assginment: Flask Feedback
"""

#Create all tables 
db.drop_all()
db.create_all()

#Entering our starter data
# return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)


U1 = User.register("mahad", "test", "mahado14@gmail.com","mahad","osman")
db.session.add(U1)
db.session.commit()


