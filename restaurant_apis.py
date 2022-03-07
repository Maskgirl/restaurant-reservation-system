import json
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import and_

from models import *
from common import db
from utils import *

restaurant_apis_blueprint = Blueprint('restaurant_apis', __name__)


@restaurant_apis_blueprint.route('/addRestaurant', methods=['POST'])
@login_required
def add_restaurant_api():
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
                                         start_datetime=datetime(2022, 2, 28, 5, 0, 0, 0),
                                         end_datetime=datetime(2022, 2, 28, 11, 0, 0, 0)
                                         )
    db.session.add(unbooked_tables_obj)
    db.session.commit()
    return {
        'status': True
    }


@restaurant_apis_blueprint.route('/removeRestaurant/<int:restaurant_id>')
def remove_restaurant(restaurant_id):
    restaurant_obj = Restaurant.query.filter_by(id=restaurant_id).first()
    db.session.delete(restaurant_obj)
    db.session.commit()
    return {
        'status': True
    }


@restaurant_apis_blueprint.route('/getAllRestaurants', methods=['GET'])
def get_all_restaurants_api():
    restaurants = get_all_restaurants()
    return {
        'status': True,
        'data': restaurants
    }


@restaurant_apis_blueprint.route('/getUnbookedTablesForRestaurant/<int:restaurant_id>', methods=['GET'])
def get_unbooked_tables_for_restaurant_api(restaurant_id):
    tables = get_unbooked_tables_for_restaurant(restaurant_id)
    return {
        'status': True,
        'data': tables
    }


@restaurant_apis_blueprint.route('/bookTables', methods=['POST'])
@login_required
def book_tables_api():
    restaurant_id = request.form['restaurant_id']
    user_id = current_user.id
    no_of_2_chairs_table = int(request.form['no_of_2_chairs_table'])
    no_of_4_chairs_table = int(request.form['no_of_4_chairs_table'])
    no_of_6_chairs_table = int(request.form['no_of_6_chairs_table'])
    no_of_12_chairs_table = int(request.form['no_of_12_chairs_table'])
    start_datetime = datetime.fromisoformat(request.form['start_datetime'])
    end_datetime = datetime.fromisoformat(request.form['end_datetime'])

    if no_of_2_chairs_table == 0 \
            and no_of_4_chairs_table == 0 \
            and no_of_6_chairs_table == 0 \
            and no_of_12_chairs_table == 0:
        return {
            'status': False,
            'message': 'Wrong inputs.'
        }

    unbooked_tables_cur = UnbookedTables.query.filter(and_(UnbookedTables.start_datetime <= start_datetime,
                                                           UnbookedTables.end_datetime >= end_datetime,
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

    new_unbooked_tables_obj_list = get_new_unbooked_tables_obj_list_after_booking(unbooked_tables_obj, start_datetime,
                                                                                  end_datetime)

    for new_unbooked_tables_obj in new_unbooked_tables_obj_list:
        db.session.add(new_unbooked_tables_obj)

    if no_of_2_chairs_table != unbooked_tables_obj.no_of_2_chairs_table \
            and no_of_4_chairs_table != unbooked_tables_obj.no_of_4_chairs_table \
            and no_of_6_chairs_table != unbooked_tables_obj.no_of_6_chairs_table \
            and no_of_12_chairs_table != unbooked_tables_obj.no_of_12_chairs_table:
        unbooked_tables_obj.start_datetime = start_datetime
        unbooked_tables_obj.end_datetime = end_datetime
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
                                     start_datetime=start_datetime,
                                     end_datetime=end_datetime
                                     )
    db.session.add(booked_tables_obj)
    db.session.commit()
    db.session.flush()

    return {
        'status': True
    }


@restaurant_apis_blueprint.route('/getBookedTablesForRestaurant/<int:restaurant_id>', methods=['GET'])
def get_booked_tables_for_restaurant_api(restaurant_id):
    tables = get_booked_tables_for_restaurant(restaurant_id)
    return {
        'status': True,
        'data': tables
    }


@restaurant_apis_blueprint.route('/getBookedTablesForUser/<int:user_id>', methods=['GET'])
@login_required
def get_booked_tables_for_user_api(user_id):
    if user_id != current_user.id:
        return {
            'status': False,
            'message': 'access denied.'
        }
    tables = get_booked_tables_for_user(user_id)
    return {
        'status': True,
        'data': tables
    }


@restaurant_apis_blueprint.route('/getUnbookedTablesWithPartySize/<int:party_size>', methods=['GET'])
def get_unbooked_tables_with_party_size_api(party_size):
    tables = get_unbooked_tables_with_party_size(party_size)
    return {
        'status': True,
        'data': tables
    }


@restaurant_apis_blueprint.route('/getUnbookedTablesWithPartySizeAndDuration/<int:party_size>/<int:duration>',
                                 methods=['GET'])
def get_unbooked_tables_with_party_size_and_duration(party_size, duration):
    tables = get_unbooked_tables_with_party_size_and_duration(party_size, duration)
    return {
        'status': True,
        'data': tables
    }
