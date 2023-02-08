from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

"""
Author: Mahad Osman
Date: Feb 7, 2023
Assginment: Flask Feedback
"""

class UserForm(FlaskForm):
    """Our Register/Login Form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired(), Email()])
    first_name =StringField("First Name",validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Our Register/Login Form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Our Feedback form"""
    title = StringField("Title:",validators=[InputRequired(), Length(max=100)])
    content = StringField("Content:",validators=[InputRequired()])
