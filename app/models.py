from flask_login import (UserMixin)
from app.extenstions import db
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(70), nullable=False)
    about = db.Column(db.String(5000), nullable=True)
    type  = db.Column(db.String(10) , nullable=False , default='User')

    def __repr__(self) -> str:
        return '<User %r>' % self.id

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False , unique=True)

    def __repr__(self) -> str:
        return '<Category %r>' % self.id
    
    
class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55), nullable=False)
    story = db.Column(db.String(5000), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('post', cascade='all, delete-orphan'))

    post_date = db.Column(db.Date, default=db.func.current_date())

    post_owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post_owner = db.relationship('User', backref=db.backref('post', cascade='all, delete-orphan'))

    active = db.Column(db.Boolean , default=True)

    positive_ratings = db.Column(db.Integer , default=0)
    negative_rating  = db.Column(db.Integer , default=0)
    
    def __repr__(self) -> str:
        return '<Post %r>' % self.id

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    comment = db.Column(db.String(5000), nullable=False)
    comment_date = db.Column(db.Date, default=db.func.current_date())

    comment_owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    comment_owner = db.relationship('User', backref=db.backref('comment', cascade='all, delete-orphan'))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref('comment', cascade='all, delete-orphan'))

    def __repr__(self) -> str:
        return '<Comment %r>' % self.id