import json
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import and_

import restaurant
from models import *
from common import db

restaurant = Blueprint('restaurant', __name__)


@restaurant.route('/addRestaurant', methods=['POST'])
@login_required
def add_restaurant():
    restaurant_obj = Restaurant(name=request.form['name'],
                                desc=request.form['desc'],
                                no_of_2_chairs_table=request.form['no_of_2_chairs_table'],
                                no_of_4_chairs_table=request.form['no_of_4_chairs_table'],
                                no_of_6_chairs_table=request.form['no_of_6_chairs_table'],
                                no_of_12_chairs_table=request.form['no_of_12_chairs_table'])

    db.session.add(restaurant_obj)
    db.session.flush()
    db.session.refresh(restaurant_obj)
    unbooked_tables_obj = UnbookedTables(restaurant_id=restaurant_obj.id,
                                         no_of_2_chairs_table=request.form['no_of_2_chairs_table'],
                                         no_of_4_chairs_table=request.form['no_of_4_chairs_table'],
                                         no_of_6_chairs_table=request.form['no_of_6_chairs_table'],
                                         no_of_12_chairs_table=request.form['no_of_12_chairs_table'],
                                         start_timestamp=datetime(2022, 2, 28, 5, 0, 0, 0),
                                         end_timestamp=datetime(2022, 2, 28, 11, 0, 0, 0)
                                         )
    db.session.add(unbooked_tables_obj)
    db.session.commit()
    return {
        'status': True
    }


@restaurant.route('/removeRestaurant/<int:restaurant_id>')
def remove_restaurant(restaurant_id):
    restaurant_obj = Restaurant.query.filter_by(id=restaurant_id).first()
    db.session.delete(restaurant_obj)
    db.session.commit()
    return {
        'status': True
    }


@restaurant.route('/getAllRestaurants', methods=['GET'])
def get_all_restaurants():
    all_restaurants = [i.to_dict() for i in Restaurant.query.all()]
    return {
        'status': True,
        'data': all_restaurants
    }


@restaurant.route('/getUnbookedTablesForRestaurant/<int:restaurant_id>', methods=['GET'])
def get_unbooked_tables_for_restaurant(restaurant_id):
    tables = [i.to_dict() for i in UnbookedTables.query.filter_by(restaurant_id=restaurant_id)]
    return {
        'status': True,
        'data': tables
    }


@restaurant.route('/bookTables', methods=['POST'])
@login_required
def book_tables():
    restaurant_id = request.form['restaurant_id']
    user_id = current_user.id
    no_of_2_chairs_table = int(request.form['no_of_2_chairs_table'])
    no_of_4_chairs_table = int(request.form['no_of_4_chairs_table'])
    no_of_6_chairs_table = int(request.form['no_of_6_chairs_table'])
    no_of_12_chairs_table = int(request.form['no_of_12_chairs_table'])
    start_timestamp = datetime.fromisoformat(request.form['start_timestamp'])
    end_timestamp = datetime.fromisoformat(request.form['end_timestamp'])

    if no_of_2_chairs_table == 0 \
            and no_of_4_chairs_table == 0 \
            and no_of_6_chairs_table == 0 \
            and no_of_12_chairs_table == 0:
        return {
            'status': False,
            'message': 'Wrong inputs.'
        }

    unbooked_tables_cur = UnbookedTables.query.filter(and_(UnbookedTables.start_timestamp <= start_timestamp,
                                                           UnbookedTables.end_timestamp >= end_timestamp,
                                                           UnbookedTables.no_of_2_chairs_table > no_of_2_chairs_table,
                                                           UnbookedTables.no_of_4_chairs_table > no_of_4_chairs_table,
                                                           UnbookedTables.no_of_6_chairs_table > no_of_6_chairs_table,
                                                           UnbookedTables.no_of_12_chairs_table > no_of_12_chairs_table)
                                                      )

    if unbooked_tables_cur.count() == 0:
        return {
            'status': False,
            'message': 'unbooked tables are not available.'
        }

    unbooked_tables_obj = unbooked_tables_cur[0]

    unbooked_tables_dict = unbooked_tables_obj.to_dict()

    new_unbooked_tables_obj_list = []
    if unbooked_tables_dict['start_timestamp'] == str(start_timestamp) \
            and unbooked_tables_dict['end_timestamp'] != str(end_timestamp):
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_timestamp=end_timestamp,
                                                           end_timestamp=unbooked_tables_obj.end_timestamp
                                                           ))
    elif unbooked_tables_dict['end_timestamp'] == str(end_timestamp) \
            and unbooked_tables_dict['start_timestamp'] != str(start_timestamp):
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_timestamp=unbooked_tables_obj.start_timestamp,
                                                           end_timestamp=start_timestamp
                                                           ))
    elif unbooked_tables_dict['end_timestamp'] != str(end_timestamp) \
            and unbooked_tables_dict['start_timestamp'] != str(start_timestamp):
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_timestamp=end_timestamp,
                                                           end_timestamp=unbooked_tables_obj.end_timestamp
                                                           ))
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_timestamp=unbooked_tables_obj.start_timestamp,
                                                           end_timestamp=start_timestamp
                                                           ))

    for new_unbooked_tables_obj in new_unbooked_tables_obj_list:
        db.session.add(new_unbooked_tables_obj)

    if no_of_2_chairs_table != unbooked_tables_obj.no_of_2_chairs_table \
            and no_of_4_chairs_table != unbooked_tables_obj.no_of_4_chairs_table \
            and no_of_6_chairs_table != unbooked_tables_obj.no_of_6_chairs_table \
            and no_of_12_chairs_table != unbooked_tables_obj.no_of_12_chairs_table:
        unbooked_tables_obj.start_timestamp = start_timestamp
        unbooked_tables_obj.end_timestamp = end_timestamp
        unbooked_tables_obj.no_of_2_chairs_table -= no_of_2_chairs_table
        unbooked_tables_obj.no_of_4_chairs_table -= no_of_4_chairs_table
        unbooked_tables_obj.no_of_6_chairs_table -= no_of_6_chairs_table
        unbooked_tables_obj.no_of_12_chairs_table -= no_of_12_chairs_table
        db.session.add(unbooked_tables_obj)
    else:
        db.session.delete(unbooked_tables_obj)

    booked_tables_obj = BookedTables(restaurant_id=restaurant_id,
                                     user_id=user_id,
                                     no_of_2_chairs_table=no_of_2_chairs_table,
                                     no_of_4_chairs_table=no_of_4_chairs_table,
                                     no_of_6_chairs_table=no_of_6_chairs_table,
                                     no_of_12_chairs_table=no_of_12_chairs_table,
                                     start_timestamp=start_timestamp,
                                     end_timestamp=end_timestamp
                                     )
    db.session.add(booked_tables_obj)
    db.session.commit()
    db.session.flush()

    return {
        'status': True
    }

    # tables = BookedTables.query.filter_by(restaurant_id=restaurant_id).to_dict()
    # return tables


@restaurant.route('/getBookedTablesForRestaurant/<int:restaurant_id>', methods=['GET'])
def get_booked_tables_for_restaurant(restaurant_id):
    tables = [i.to_dict() for i in BookedTables.query.filter_by(restaurant_id=restaurant_id)]
    return {
        'status': True,
        'data': tables
    }


@restaurant.route('/getBookedTablesForUser/<int:user_id>', methods=['GET'])
@login_required
def get_booked_tables_for_user(user_id):
    if user_id != current_user.id:
        return {
            'status': False,
            'message': 'access denied.'
        }
    tables = [i.to_dict() for i in BookedTables.query.filter_by(user_id=user_id)]
    return {
        'status': True,
        'data': tables
    }


@restaurant.route('/getUnbookedTablesWithPartySize/<int:user_id>', methods=['GET'])
def get_unbooked_tables_with_party_size(party_size):
    tables = db.engine.execute(f"select * from unbooked_tables "
                               f"where "
                               f"2*no_of_2_chairs_table+"
                               f"4*no_of_4_chairs_table+"
                               f"6*no_of_6_chairs_table+"
                               f"12*no_of_12_chairs_table>={party_size}'")
    return {
        'status': True,
        'data': tables
    }


@restaurant.route('/getUnbookedTablesWithPartySizeAndDuration/<int:user_id>', methods=['GET'])
def get_unbooked_tables_with_party_size_and_duration(party_size, duration):
    tables = db.engine.execute(f"select *, DATEDIFF(second, start_timestamp, end_timestamp) AS duration "
                               f"from unbooked_tables "
                               f"where duration>={duration}"
                               f"2*no_of_2_chairs_table+"
                               f"4*no_of_4_chairs_table+"
                               f"6*no_of_6_chairs_table+"
                               f"12*no_of_12_chairs_table>={party_size}'")
    return {
        'status': True,
        'data': tables
    }
