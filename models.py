"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType
from datetime import datetime

DEFAULT_IMAGE_URL = None

db = SQLAlchemy()


def connect_db(app):
    """connect to database"""
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

# TODO: update default image
    image_url = db.Column(
        URLType,
        default=DEFAULT_IMAGE_URL
    )


class Post(db.Model):
    """Post"""
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(50),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship('User', backref='posts')