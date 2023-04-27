"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType

DEFAULT_IMAGE_URL = 'https://staticg.sportskeeda.com/editor/2021/12/7f3a3-16401713211125-1920.jpg'

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
