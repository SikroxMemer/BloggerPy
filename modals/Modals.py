from flask_login import (UserMixin)
from __main__ import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    about = db.Column(db.String(5000), nullable=True)

    def __repr__(self) -> str:
        return '<User %r>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> str:
        return '<Category %r>' % self.id

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55), nullable=False)
    story = db.Column(db.String(5000), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref(
        'post', cascade='all, delete-orphan'))

    post_date = db.Column(db.Date, default=db.func.current_date())

    post_owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post_owner = db.relationship('User', backref=db.backref(
        'post', cascade='all, delete-orphan'))

    def __repr__(self) -> str:
        return '<Post %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(150), nullable=False)

    comment_date = db.Column(db.Date, default=db.func.current_date())
    comment_owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    comment_owner = db.relationship('User', backref=db.backref(
        'comment', cascade='all, delete-orphan'))

    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref(
        'comment', cascade='all, delete-orphan'))

    def __repr__(self) -> str:
        return '<Comment %r>' % self.id


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref(
        'rating', cascade='all, delete-orphan'))
    positive = db.Column(db.Integer, default=0)
    negative = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref(
        'rating', cascade='all, delete-orphan'))
