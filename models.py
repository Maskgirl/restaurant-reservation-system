__all__ = ['Restaurant', 'User', 'UnbookedTables', 'BookedTables']

from datetime import datetime

from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from common import db


class Restaurant(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    no_of_2_chairs_table = db.Column(db.Integer)
    no_of_4_chairs_table = db.Column(db.Integer)
    no_of_6_chairs_table = db.Column(db.Integer)
    no_of_12_chairs_table = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, SerializerMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(55), nullable=False)
    last_name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(144))
    password = db.Column(db.String(144))
    phone = db.Column(db.String(12))
    address = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class UnbookedTables(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    no_of_2_chairs_table = db.Column(db.Integer)
    no_of_4_chairs_table = db.Column(db.Integer)
    no_of_6_chairs_table = db.Column(db.Integer)
    no_of_12_chairs_table = db.Column(db.Integer)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class BookedTables(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    no_of_2_chairs_table = db.Column(db.Integer)
    no_of_4_chairs_table = db.Column(db.Integer)
    no_of_6_chairs_table = db.Column(db.Integer)
    no_of_12_chairs_table = db.Column(db.Integer)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
