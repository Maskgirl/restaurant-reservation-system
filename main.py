# main.py

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from utils import *

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('restaurant.search'))


@main_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=f'{current_user.first_name} {current_user.last_name}')
