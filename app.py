"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from models import connect_db, User, Post, db, DEFAULT_IMAGE_URL
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
    image_url = request.form.get('image_url',DEFAULT_IMAGE_URL)

    new_user = User(first_name = first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash("User added!")
    return redirect('/users')


@app.get('/users/<int:user_id>')
def render_user_details(user_id):
    """render the details page for a single user"""

    user = User.query.get(user_id)
    author = User.query.get(user_id)
    posts = author.posts

    return render_template('user_detail.html',
                           user=user,
                           posts=posts)


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

    flash("User info edited")
    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ handles deleting user """

    user = User.query.get_or_404(user_id)

    posts = user.posts
    for post in posts:
        db.session.delete(post)
        db.session.commit()

    db.session.delete(user)
    db.session.commit()

    flash("User deleted!")
    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def new_post_page(user_id):
    """show new post page"""

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html',
                           user=user)


@app.post('/users/<int:user_id>/posts/new')
def added_new_post(user_id):
    """adding new post"""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    flash("New post added!")
    return redirect(f"/users/{user_id}")


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """shows an individual post page"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post_detail.html', user=user, post=post)


@app.get('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """shows the page to edit a post"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('edit_post.html', user=user, post=post)


@app.post('/posts/<int:post_id>/edit')
def handle_edit(post_id):
    """edit a post"""

    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    flash('Post edited')
    return redirect(f'/posts/{post_id}')


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted!')
    return redirect(f'/users/{user.id}')



