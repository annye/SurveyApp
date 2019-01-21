from datetime import datetime
from hashlib import md5
#from flask import UserMixin
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from SurveyApp import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

        
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)







class enduser(db.Model):
    __tablename__ = 'endusers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    nationality = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, name, nationality, gender, age):
        self.name= name
        self.nationality= nationality
        self.gender = gender
        self.age= age


class Arglist(db.Model):
    __tablename__ ='arglist'
    id = db.Column(db.Integer, primary_key=True)
    side = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    claim = db.Column(db.String(200), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, side, title, claim):
        self.side=side
        self.title=title
        self.claim=claim


