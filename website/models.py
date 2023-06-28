from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_source = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mimetype = db.Column(db.Text)
    # If it is python we can use User.id but since we are using Sql we use 'user.id'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # creating a relationship with the images table
    images = db.relationship('Image')
