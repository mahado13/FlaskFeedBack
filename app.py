from crypt import methods
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from form import UserForm, LoginForm, FeedbackForm

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
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        fn = form.first_name.data
        ln = form.last_name.data

        new_user =  User.register(username,password,email,fn,ln)
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Logging a new user"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data    
        user = User.authenticate(username, password)
        if user:
            flash(f"Sucessful Login: {user.username}", 'Success')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid login information']
    return render_template('login.html', form = form)


@app.route('/users/<string:username>', methods=['GET'])
def secret(username):
    """Our secret page that only logged in users can view"""
    if 'username' not in session:
        flash("Please Login first", 'danger')
        return redirect('/')
    
    user = User.query.get_or_404(username)
    user_feedback = user.feedback #retrieves a list of feedback based on our user
    return render_template('secret.html', user=user, user_feedback=user_feedback)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username')
    flash('Goodbye', 'info')
    return redirect('/')

@app.route('/users/<string:username>/add', methods=['GET','POST'])
def add_user(username):
    """A path to both provide a form to add our users
       - While also handling the adding function
    """
    return render_template('')

@app.route('/users/<string:username>/edit', methods=['GET','POST'])
def edit_user(username):
    """A path to both provide a form to edit our users
       - While also handling the editing function
    """
    return render_template('')

@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    """A path to remove a user from our database
        - Also confirms if a user first exists
        - Will also delete all of their feedback
    """
    if 'username' not in session:
        flash("Please Login first", 'danger')
        return redirect('/')

    session.pop('username') 
    user = User.query.get(username)
    user_feedback = user.feedback
    for feedback in user_feedback:
        db.session.delete(feedback)
        db.session.commit()
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {username} has been deleted', 'success')
    return redirect('/')

@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """ A path to render a feedback form
        - As well as handle it's submission
    """
    if 'username' not in session:
        flash("Please Login first", 'danger')
        return redirect('/')

    user = User.query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')
    else:
        return render_template('add_feedback.html',user=user,form=form)

@app.route('/feedback/<int:id>/edit', methods=['GET', 'POST'])
def edit_feedback(id):
    """ A path that allows us to render our edit feedback form
        - As well as handle it's submission
    """
    if 'username' not in session:
        flash("Please Login first", 'danger')
        return redirect('/')
    
    username = session['username']
    feedback = Feedback.query.get_or_404(id)

    #Confirming the logged in user can only edit their own
    if username != feedback.username:
        flash("You cannot edit another users feedback", 'danger')
        return redirect('/')
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('edit_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """ A path that will allow us to delete feedback
        - Error checking in place to confirm a user must be logged in
    """
    if 'username' not in session:
        flash("Please Login first", 'danger')
        return redirect('/')
    
    username = session['username']
    feedback = Feedback.query.get_or_404(id)

    if username != feedback.username:
        flash("You cannot delete another users feedback", 'danger')
        return redirect('/')


    db.session.delete(feedback)
    db.session.commit()
    flash(f'Sucessfully delete: {feedback.title}', 'info')
    return redirect(f'/users/{username}')
    
