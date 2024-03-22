from flask_login import (UserMixin)
from app.extenstions import db

class User(db.Model, UserMixin):
    """
    The User class inherits from db.Model and UserMixin.
    id, username, password, profile_picture, email, and about are attributes of the User class.
    The __repr__ method returns a string representation of the user with their ID.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    about = db.Column(db.String(5000), nullable=True)

    def __repr__(self) -> str:
        return '<User %r>' % self.id


class Category(db.Model):
    """
    The Category class represents a database table for categories.
    The id method defines an integer column as the primary key.
    The title method defines a string column with a maximum length of 25 characters and it cannot be null.
    The __repr__ method returns a string representation of the category object, including its id.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> str:
        return '<Category %r>' % self.id


class Post(db.Model):
    """
    This class definition represents a Post entity with the following methods:
    __repr__(self): Returns a string representation of the Post object.
    It returns a string with the Post ID for debugging and logging purposes.
    """
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
    """
    This class definition creates a model for a comment in a database.
    id: Represents the unique identifier of the comment.
    comment: Represents the actual content of the comment.
    comment_date: Represents the date the comment was created.
    comment_owner_id: Represents the foreign key relationship with the user who owns the comment.
    comment_owner: Represents the relationship with the User model.
    post_id: Represents the foreign key relationship with the post the comment belongs to.
    post: Represents the relationship with the Post model.
    __repr__(self): Returns a string representation of the Comment object.
    """
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(5000), nullable=False)

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
    id = db.Column(db.Integer , primary_key=True)
    positiveRate = db.Column(db.Boolean)
    negativeRate = db.Column(db.Boolean)
    user = db.relationship(
        'User' , 
        backref=db.backref(
            'ratings' , 
            cascade='all , delete-orphan'
    ))
    def __repr__(self) -> str:
        return '<Rating %r>' % self.id