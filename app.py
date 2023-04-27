"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from models import connect_db, User, db
from flask_sqlalchemy import SQLAlchemy

from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def redirect_users():
    """ Redirect home page to users page """

    return redirect('/users')

@app.get('/users')
def get_users():
    """ Show list of users """

    users = User.query.all()

    return render_template('users.html',
                           users=users)

@app.get('/users/new')
def render_add_user():
    """ render the add user page """
    return render_template('add_user.html')


@app.post('/users/new')
def process_add_user():
    """process the add user form to add a new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    print(f"REQUEST FORM: {request.form}")
    image_url = request.form['image_url']
# TODO: update default image
    new_user = User(first_name = first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def render_user_details(user_id):
    """render the details page for a single user"""

    user = User.query.get(user_id)

    return render_template('user_detail.html', user=user )

@app.get('/users/<int:user_id>/edit')
def render_edit_user(user_id):
    """ render edit user page """

    user = User.query.get(user_id)

    return render_template('edit_user.html',
                           user=user)

@app.post('/users/<int:user_id>/edit')
def process_user_edit(user_id):
    """ process user edit and redirect to /user page """

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ handles deleting user """
# TODO: always use get_or_404
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')