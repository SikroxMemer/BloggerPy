from flask_login import (UserMixin)
from app.extenstions import db

class Admin(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    def __repr__(self) -> str:
        return '<Admin %r>' % self.id