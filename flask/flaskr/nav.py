from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import psycopg2.extras

bp = Blueprint('nav', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return redirect(url_for('home.home'))


'''
@bp.route('/search')
##@login_required
def search():
    return render_template('search/search.html')
'''

# @bp.route('/studies')
# @login_required
# def studies():
#     return render_template('study/studies.html')


