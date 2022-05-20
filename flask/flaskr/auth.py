import functools
from psycopg2._psycopg import IntegrityError
import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            print(user)
            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
        except:
            error = 'Error: unable to fetch data'
            flash(error)

        session.clear()
        session['user'] = user
        cur.execute("UPDATE currentFlaskUser SET flaskUser =%s",(user[1],))
        conn.commit()
        print("lamoooooooooooooooo")
        return redirect(url_for('home.home'))
    return render_template('auth/login.html')

'''
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM users Where username = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
'''
@bp.before_app_request
def load_logged_in_user():
    user = session.get('user')

    if user is None:
        g.user = None
        return

    g.user = user


@bp.route('/logout')
def logout():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("UPDATE currentFlaskUser SET flaskUser =%s",('not-logged-in',))
    conn.commit()
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
