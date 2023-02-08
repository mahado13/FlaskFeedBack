from models import db, connect_db, User, Feedback
from app import app


"""
Author: Mahad Osman
Date: Feb 7, 2023
Assginment: Flask Feedback
"""

#Create all tables 
db.drop_all()
db.create_all()

#User Template(Template)
#User(username="", password="", email="", first_name="", last_name="")

#Entering our starter data 
U1 = User.register("mahad", "test", "mahado14@gmail.com","mahad","osman")
db.session.add(U1)
db.session.commit()


#Feedback Template
F1 = Feedback(title="Test article",content="This is our fist feedback", username="mahad")
F2 = Feedback(title="Test article 2",content="This is our second feedback", username="mahad")

db.session.add_all([F1, F2])
db.session.commit()


