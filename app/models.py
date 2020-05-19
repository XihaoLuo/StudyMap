from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Building(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    studySpaces = db.relationship('StudySpace', \
                    backref = 'building', lazy = 'dynamic')

    def __repr__(self):
        return '<Building {}>'.format(self.name)

class StudySpace(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    post = db.relationship('Post', backref = 'studySpace', lazy = 'dynamic')

    def __repr__(self):
        return '<StudySpace {}>'.format(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy = 'dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {} - email: {}>'.format(self.username, self.email)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    building = db.Column(db.String(64)) # this is for check-in/check-out
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # many to one relationship w/ StudySpace
    studySpace_id = db.Column(db.Integer, db.ForeignKey('study_space.id'))

    def __repr__(self):
        return '<Post {} - Building: {} \
                Timestamp:{}>'.format(self.body, self.building, self.timestamp)
