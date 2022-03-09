import datetime
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from models import *

if os.path.exists('db.sqlite'):
    os.remove("db.sqlite")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine('sqlite:///db.sqlite', echo=True)

meta = MetaData()

Table(
    'restaurant', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('desc', String, nullable=False),
    Column("no_of_2_chairs_table", Integer),
    Column("no_of_4_chairs_table", Integer),
    Column("no_of_6_chairs_table", Integer),
    Column("no_of_12_chairs_table", Integer),
    Column("date_created", DateTime, nullable=False)
)

Table(
    'user', meta,
    Column('id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String),
    Column('password', String),
    Column('phone', String),
    Column('address', String),
    Column("date_created", DateTime, nullable=False)
)

Table(
    'unbooked_tables', meta,
    Column('id', Integer, primary_key=True),
    Column('restaurant_id', Integer, nullable=False),
    Column("no_of_2_chairs_table", Integer),
    Column("no_of_4_chairs_table", Integer),
    Column("no_of_6_chairs_table", Integer),
    Column("no_of_12_chairs_table", Integer),
    Column("start_datetime", DateTime, nullable=False),
    Column("end_datetime", DateTime, nullable=False),
    Column("date_created", DateTime, nullable=False)
)

Table(
    'booked_tables', meta,
    Column('id', Integer, primary_key=True),
    Column('restaurant_id', Integer, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column("no_of_2_chairs_table", Integer, nullable=False),
    Column("no_of_4_chairs_table", Integer),
    Column("no_of_6_chairs_table", Integer),
    Column("no_of_12_chairs_table", Integer),
    Column("start_datetime", DateTime, nullable=False),
    Column("end_datetime", DateTime, nullable=False),
    Column("date_created", DateTime, nullable=False)
)

meta.create_all(engine)

restaurants = [
    {
        'name': 'Foodie_Tech',
        'desc': '"Eating is like Coding, Never Ending."',
        'no_of_2_chairs_table': 21,
        'no_of_4_chairs_table': 13,
        'no_of_6_chairs_table': 8,
        'no_of_12_chairs_table': 5,
    },
    {
        'name': 'Burger King',
        'desc': 'Eat Burger',
        'no_of_2_chairs_table': 3,
        'no_of_4_chairs_table': 5,
        'no_of_6_chairs_table': 8,
        'no_of_12_chairs_table': 1,
    },
    {
        'name': 'Domino\'s',
        'desc': 'Eat Pizza',
        'no_of_2_chairs_table': 3,
        'no_of_4_chairs_table': 5,
        'no_of_6_chairs_table': 8,
        'no_of_12_chairs_table': 1,
    },
    {
        'name': 'Pani-Puri',
        'desc': 'Eat Pani-Puri',
        'no_of_2_chairs_table': 10,
        'no_of_4_chairs_table': 2,
        'no_of_6_chairs_table': 1,
        'no_of_12_chairs_table': 0,
    }
]

for restaurant in restaurants:
    restaurant_obj = Restaurant(name=restaurant['name'],
                                desc=restaurant['desc'],
                                no_of_2_chairs_table=restaurant['no_of_2_chairs_table'],
                                no_of_4_chairs_table=restaurant['no_of_4_chairs_table'],
                                no_of_6_chairs_table=restaurant['no_of_6_chairs_table'],
                                no_of_12_chairs_table=restaurant['no_of_12_chairs_table'])

    db.session.add(restaurant_obj)
    db.session.flush()
    db.session.refresh(restaurant_obj)
    unbooked_tables_obj = UnbookedTables(restaurant_id=restaurant_obj.id,
                                         no_of_2_chairs_table=restaurant['no_of_2_chairs_table'],
                                         no_of_4_chairs_table=restaurant['no_of_4_chairs_table'],
                                         no_of_6_chairs_table=restaurant['no_of_6_chairs_table'],
                                         no_of_12_chairs_table=restaurant['no_of_12_chairs_table'],
                                         start_datetime=datetime.datetime(year=2022, month=3, day=9, hour=0, minute=0),
                                         end_datetime=datetime.datetime(year=2022, month=3, day=29, hour=0, minute=0),
                                         )
    db.session.add(unbooked_tables_obj)
    db.session.commit()
