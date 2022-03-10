import json
from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, g
from flask_login import login_required, current_user
from sqlalchemy import and_
import stringcase
from models import *
from common import db
from utils import *

restaurant_blueprint = Blueprint('restaurant', __name__)


@restaurant_blueprint.route('/search')
@login_required
def search():
    g.active_page = "search"
    args = request.args.to_dict()
    if 'party_size' not in args or 'hours' not in args or 'minutes' not in args:
        args = {
            'party_size': 2,
            'hours': 1,
            'minutes': 0,
            'start_datetime': "2022-03-09T00:00",
            'end_datetime': "2022-03-29T00:00"
        }
    party_size = args['party_size']
    hours = int(args['hours'])
    minutes = int(args['minutes'])
    duration = hours * 60 * 60 + 60 * minutes
    start_datetime = datetime.strptime(args['start_datetime'], '%Y-%m-%dT%H:%M')
    end_datetime = datetime.strptime(args['end_datetime'], '%Y-%m-%dT%H:%M')
    tables = get_unbooked_tables_with_party_size_and_duration(party_size, duration, start_datetime, end_datetime)
    return render_template('search.html', args=args, tables=tables, stringcase=stringcase)


@restaurant_blueprint.route('/bookNow', methods=['GET', 'POST'])
@login_required
def book_now():
    g.active_page = "book_now"
    if request.method == "POST":
        unbooked_tables_id = int(request.form['unbooked_tables_id'])
        unbooked_tables = get_unbooked_tables(unbooked_tables_id)

        # To convert python datetime to html input type datetime-local format
        unbooked_tables['start_datetime'] = python_datetime_to_html_input_tag_datetime_local(
            datetime.fromisoformat(unbooked_tables['start_datetime']))
        unbooked_tables['end_datetime'] = python_datetime_to_html_input_tag_datetime_local(
            datetime.fromisoformat(unbooked_tables['end_datetime']))

        no_of_2_chairs_table = int(request.form['no_of_2_chairs_table'])
        no_of_4_chairs_table = int(request.form['no_of_4_chairs_table'])
        no_of_6_chairs_table = int(request.form['no_of_6_chairs_table'])
        no_of_12_chairs_table = int(request.form['no_of_12_chairs_table'])

        start_datetime = datetime.fromisoformat(request.form['start_datetime'])
        end_datetime = datetime.fromisoformat(request.form['end_datetime'])

        restaurant_name = get_restaurant_details(unbooked_tables['restaurant_id'])['name']
        res = book_tables(
            unbooked_tables_id,
            current_user.id,
            no_of_2_chairs_table,
            no_of_4_chairs_table,
            no_of_6_chairs_table,
            no_of_12_chairs_table,
            start_datetime,
            end_datetime)
        return render_template('book_now.html',
                               unbooked_tables_id=unbooked_tables_id,
                               unbooked_tables=unbooked_tables,
                               start_datetime=python_datetime_to_html_input_tag_datetime_local(start_datetime),
                               end_datetime=python_datetime_to_html_input_tag_datetime_local(end_datetime),
                               restaurant_name=restaurant_name,
                               no_of_2_chairs_table=no_of_2_chairs_table,
                               no_of_4_chairs_table=no_of_4_chairs_table,
                               no_of_6_chairs_table=no_of_6_chairs_table,
                               no_of_12_chairs_table=no_of_12_chairs_table,
                               res=res)

    unbooked_tables_id = int(request.args.get('unbooked_tables_id'))
    unbooked_tables = get_unbooked_tables(unbooked_tables_id)

    # To convert python datetime to html input type datetime-local format
    unbooked_tables['start_datetime'] = python_datetime_to_html_input_tag_datetime_local(
        datetime.fromisoformat(unbooked_tables['start_datetime']))
    unbooked_tables['end_datetime'] = python_datetime_to_html_input_tag_datetime_local(
        datetime.fromisoformat(unbooked_tables['end_datetime']))

    restaurant_name = get_restaurant_details(unbooked_tables['restaurant_id'])['name']

    return render_template('book_now.html',
                           unbooked_tables_id=unbooked_tables_id,
                           unbooked_tables=unbooked_tables,
                           start_datetime=unbooked_tables['start_datetime'],
                           end_datetime=unbooked_tables['end_datetime'],
                           restaurant_name=restaurant_name,
                           no_of_2_chairs_table=2,
                           no_of_4_chairs_table=0,
                           no_of_6_chairs_table=0,
                           no_of_12_chairs_table=0,
                           res={})
