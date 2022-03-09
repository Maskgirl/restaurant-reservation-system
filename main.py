# main.py

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, g
from flask_login import login_required, current_user
from utils import *
import stringcase

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('restaurant.search'))


@main_blueprint.route('/my_booking')
@login_required
def my_booking():
    g.active_page = "my_booking"
    tables = get_user_bookings(current_user.id)
    return render_template('my_bookings.html', tables=tables, stringcase=stringcase)
