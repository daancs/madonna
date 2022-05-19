from datetime import datetime
from deepdiff import DeepDiff
import json

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
    searchHistory = cur.fetchall()

    cur.execute("SELECT tstamp, operation, who, new_val, old_val FROM changeLog")
    changeLog = []
    for entry in cur.fetchall():
        changeLog.append(changeLogParser(entry))

    print(changeLog)
    # if g.user is None:
        # return redirect(url_for('auth.login'))
    # else:
    return render_template('home/home.html', searchHistory=searchHistory, changeLog=changeLog)


def changeLogParser(entry):
    out = entry
    out[0] = entry[0].strftime("%Y-%m-%d %H:%M:%S")
    print(entry[3]['key_id'])
    diff = DeepDiff(entry[3], entry[4])
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
    print(json.dumps(diff, indent=4))
    return out
