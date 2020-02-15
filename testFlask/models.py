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
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    full_name = db.Column(db.String(100))


class Room(db.Model):
    __tablename__ = "room"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    floor = db.Column(db.String(100))

    places = db.relationship("Place", backref="room", lazy=True)


class Place(db.Model):
    __tablename__ = "place"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.String(100))

    users = db.relationship("User", backref="place", lazy=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
