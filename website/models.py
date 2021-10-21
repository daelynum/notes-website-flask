from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView


# tables for DB
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.Date, default=func.now())

    # relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Note %r>' % self.user_id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # relationship
    notes = db.relationship('Note')

    def __repr__(self):
        return '<User %r>' % self.id


# admin view
class NoteView(ModelView):
    form_columns = ['user_id', 'data', 'date']


class UserView(ModelView):
    form_columns = ['email', 'password', 'first_name']
