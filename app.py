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