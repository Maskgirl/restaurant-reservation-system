# main.py

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from utils import *

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    args = request.args.to_dict()
    if 'party_size' in args and 'hours' in args and 'minutes' in args:
        party_size = request.args.get('party_size')
        hours = int(request.args.get('hours'))
        minutes = int(request.args.get('minutes'))
        duration = hours * 60 * 60 + 60 * minutes
        tables = get_unbooked_tables_with_party_size_and_duration(party_size, duration)
        return render_template('index_with_search.html', args=args, tables=tables)
    return render_template('index.html')


@main_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=f'{current_user.first_name} {current_user.last_name}')
