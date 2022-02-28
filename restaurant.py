import json
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import and_

from models import *

from common import db

restaurant = Blueprint('restaurant', __name__)


@restaurant.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    all_restaurants = [i.to_dict() for i in Restaurant.query.all()]
    return jsonify(all_restaurants)


@restaurant.route('/unbookedTables/<int:restaurant_id>', methods=['GET'])
def unbooked_tables(restaurant_id):
    tables = [i.to_dict() for i in UnbookedTables.query.filter_by(restaurant_id=restaurant_id)]
    return jsonify(tables)


@restaurant.route('/bookedTables/<int:restaurant_id>', methods=['GET'])
def booked_tables(restaurant_id):
    tables = [i.to_dict() for i in UnbookedTables.query.filter_by(restaurant_id=restaurant_id).to_dict()]
    return jsonify(tables)


@restaurant.route('/bookTables', methods=['POST'])
# @login_required
def book_tables():
    restaurant_id = request.form['restaurant_id']
    user_id = 1
    no_of_2_chairs_table = int(request.form['no_of_2_chairs_table'])
    no_of_4_chairs_table = int(request.form['no_of_4_chairs_table'])
    no_of_6_chairs_table = int(request.form['no_of_6_chairs_table'])
    no_of_12_chairs_table = int(request.form['no_of_12_chairs_table'])
    start_timestamp = datetime(2022, 2, 28, 6, 0, 0, 0)
    end_timestamp = datetime(2022, 2, 28, 7, 0, 0, 0)

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
    # return jsonify(tables)

# tables = db.engine.execute(f"select * from unbooked_tables "
#                                f"where start_timestamp<='{start_timestamp}'"
#                                f" and end_timestamp>='{end_timestamp}"
#                                f" and "
#                                f"2*no_of_2_chairs_table+"
#                                f"4*no_of_4_chairs_table+"
#                                f"6*no_of_6_chairs_table+"
#                                f"12*no_of_12_chairs_table>={party_size}'")
