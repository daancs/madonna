from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
import psycopg2, psycopg2.extras

from flaskr.auth import login_required
from . import db

bp = Blueprint('studies', __name__)


@bp.route('/studies')
def patients():
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM Patients RIGHT JOIN Study1 ON patients.key_id=study1.patient"
    query2 = "SELECT * FROM Patients RIGHT JOIN Study2 ON patients.key_id=study2.patient"
    cur.execute(query)
    result = cur.fetchall()
    cur.execute(query2)
    result2 = cur.fetchall()
    conn.commit()


    return render_template('study/studies.html', result=result, result2=result2)


@bp.route('/studies/studyOne')
def studyInfo():
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM Patients RIGHT JOIN Study1 ON patients.key_id=study1.patient"
    cur.execute(query)
    result = cur.fetchall()
    questions = "SELECT * FROM Surveys WHERE study=1"
    cur.execute(questions)
    result2 = cur.fetchall()
    conn.commit()

    return render_template('study/studyInfo.html', result=result, result2=result2)

@bp.route('/studies/studyTwo')
def studyInfo2():
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM Patients RIGHT JOIN Study2 ON patients.key_id=study2.patient"
    cur.execute(query)
    result = cur.fetchall()
    questions = "SELECT * FROM Surveys WHERE study=2"
    cur.execute(questions)
    result2 = cur.fetchall()
    conn.commit()

    return render_template('study/studyInfo2.html', result=result, result2=result2)


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
