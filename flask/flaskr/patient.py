from turtle import back
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
import psycopg2, psycopg2.extras

from flaskr.auth import login_required
from . import db

bp = Blueprint('patient', __name__)


@bp.route('/patient/<key_id>')
def patient(key_id):
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM Patients LEFT JOIN Cases ON patients.key_id=cases.patient WHERE Patients.key_id =(%s)"
    cur.execute(query, (key_id,))
    conn.commit()
    result = cur.fetchall()
    return render_template('patient/patientview.html', result=result[0])


""" def buildPatientQuery(key_id):
    query = SELECT * FROM Patients WHERE Patients.key_id = %s INNER JOIN Cases ON Patients.key_id=Cases.patient, (key_id,)
    return query

def runQuery(query):
    
    This function runs the query in postgresql.

    database = db.get_db()
    cur = database.cursor(cursor_factory=psycopg2.extras.DictCursor) # needed for select queries
    cur.execute(query)
    database.commit()
    res = cur.fetchall()
    return res 
"""

def exit():
    return redirect(back)
