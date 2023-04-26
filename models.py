"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType


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

    image_url = db.Column(
        URLType,
        default='',
        nullable=False
    )