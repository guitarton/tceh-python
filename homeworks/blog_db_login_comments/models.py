from datetime import datetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from database import db


class Article(db.Model):
    id = db.Column('title_id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(140), nullable=False, unique=True)
    content = db.Column('content', db.String(3000), nullable=False)
    is_visible = db.Column('is_visible', db.Boolean)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))

    user = db.relationship('User', backref=db.backref('articles', lazy='dynamic'))
    date_created = db.Column(db.Date, default=datetime.today())

    def __init__(self, title, content, user, date_created=None):
        self.title = title
        self.content = content
        self.is_visible = True
        self.user = user
        if date_created is not None:
            self.date_created = date_created


class Comment(db.Model):
    id = db.Column('comment_id', db.Integer, primary_key=True)
    content = db.Column('content', db.String(3000), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
    article_id = db.Column('article_id', db.Integer, db.ForeignKey('article.title_id'))
    article = db.relationship('Article', backref=db.backref('comments', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    date_created = db.Column(db.Date, default=datetime.today())

    def __init__(self, content, article, user=None, date_created=None):
        self.content = content
        self.article = article
        if user is not None:
            self.user = user
        if date_created is not None:
            self.date_created = date_created


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)

    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username=None, email=None):
        self.username = username
        # we do not store original password.
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %s>' % self.username
