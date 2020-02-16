from flask_login import UserMixin
from testFlask import db
import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            pole = [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']
            if "full_name" in pole:
                place = Place.query.filter_by(id=obj.place_id).first()
                fields["room"] = Room.query.filter_by(id=place.room_id).first().name
                fields["place_num"] = str(place.number)
            else:
                fields["room"] = obj.name
                fields["place_num"] = ""
            for field in pole:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


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
    full_type = db.Column(db.String(100))


class Place(db.Model):
    __tablename__ = "place"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.String(100))

    users = db.relationship("User", backref="place", lazy=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
