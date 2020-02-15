from flask_login import UserMixin
from testFlask import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy

    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    surname = db.Column(db.String(100))
    name = db.Column(db.String(100))

    place = db.relationship("Place", uselist=False, back_populates="user")


class Room(db.Model):
    __tablename__ = "room"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    floor = db.Column(db.Integer)

    place = db.relationship("Place", back_populates="room")


class Place(db.Model):
    __tablename__ = "place"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.Integer)

    user = db.relationship("User", back_populates="place")
    room = db.relationship("Room", back_populates="place")
