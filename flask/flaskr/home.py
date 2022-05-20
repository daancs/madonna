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
    cur.execute("SELECT tstamp, who, old_val, new_val FROM changeLog")
    changeLog = []
    for entry in cur.fetchall():
        changeLog.append(changeLogParser(entry))

    # print(changeLog[0][2]['values_changed'].items())

    # for foo in changeLog[0][2]['values_changed'].items():
        # print(f"values_changed: {foo[0]}")
        # for bar in foo[1]:
            # print(f"{bar}: {foo[1][bar]}")



    return render_template('home/home.html', searchHistory=searchHistory, changeLog=changeLog)


def changeLogParser(entry):
    out = []

    #Timestamp
    out.append(entry[0].strftime("%Y-%m-%d %H:%M:%S"))

    #User who made the change
    out.append(entry[1])

    # entry[3] == new_val, entry[4] == old_val
    diff = DeepDiff(entry[2], entry[3])
    # print(json.dumps(diff, indent=4))
    diff=diff.to_dict()
    out.append(diff)
    return out
