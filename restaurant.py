import json
from datetime import datetime

from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from sqlalchemy import and_

from models import *
from common import db
from utils import *

restaurant_blueprint = Blueprint('restaurant', __name__)


@restaurant_blueprint.route('/find_tables')
@login_required
def find_tables():
    args = request.args.to_dict()
    if 'party_size' in args and 'hours' in args and 'minutes' in args:
        party_size = args['party_size']
        hours = int(args['hours'])
        minutes = int(args['minutes'])
        duration = hours * 60 * 60 + 60 * minutes
        start_datetime = datetime.strptime(args['start_datetime'], '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(args['end_datetime'], '%Y-%m-%dT%H:%M')
        tables = get_unbooked_tables_with_party_size_and_duration(party_size, duration, start_datetime, end_datetime)
        return render_template('find_tables.html', args=args, tables=tables)

    return render_template('find_tables.html', args=args)
