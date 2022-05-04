from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
import psycopg2, psycopg2.extras

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/home')
@login_required
def home():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM SearchHistory")
    history = cur.fetchall()
    print(history)
    # if g.user is None:
        # return redirect(url_for('auth.login'))
    # else:
    return render_template('home/home.html', history=history)
