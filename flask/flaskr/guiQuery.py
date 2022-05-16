from traceback import print_tb
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import psycopg2, psycopg2.extras

from flaskr.auth import login_required

from . import db
# from . import queryLogger

bp = Blueprint('search', __name__)

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def index():
    """
    This function renders the query page.
    If it is a POST request it parses the query and tries to run it in postgresql.
    Otherwise it just renders the page.
    """
    result = None
    g.isResString = False

    if request.method == 'POST':
        id = request.form['key_id']
        gender = request.form['gender']
        name = request.form['name']
        weight = request.form['weight']
        age = request.form['age']
        study = request.form['study']
        ans1a = request.form['survey1a']
        ans1b = request.form['survey1b']
        ans1c = request.form['survey1c']
        ans2a = request.form['survey2a']
        ans2b = request.form['survey2b']
        ans2c = request.form['survey2c']
        ans3a = request.form['survey3a']
        ans3b = request.form['survey3b']
        ans3c = request.form['survey3c']
        try:
            nicotine = request.form['nicotine']
        except:
            nicotine = False


        query = buildQuery(id, gender, name, weight, age, nicotine, study,
                            ans1a, ans1b, ans1c,
                            ans2a, ans2b, ans2c,
                            ans3a, ans3b, ans3c)

        db.addToHistory(g.user[1], id, gender, name, weight, age, nicotine, study)

        conn = db.get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(query)

        result = cur.fetchall()
        print(result)
            # result = "Error: unable to fetch data"
            # g.isResString = True
    return render_template('/search/search.html', result=result)

def buildQuery(id, gender, name, weight, age, nicotine, study,
                ans1a, ans1b, ans1c,
                ans2a, ans2b, ans2c,
                ans3a, ans3b, ans3c):
    query = ""

    id = "%" + id + "%"
    name = "%" + name + "%"
    weight = "%" + weight + "%"
    age = "%" + age +"%"

    study = "%" + study + "%"
    ans1a = "%" + ans1a + "%"
    ans1b = "%" + ans1b + "%"
    ans1c = "%" + ans1c + "%"

    ans2a = "%" + ans2a + "%"
    ans2b = "%" + ans2b + "%"
    ans2c = "%" + ans2c + "%"

    ans3a = "%" + ans3a + "%"
    ans3b = "%" + ans3b + "%"
    ans3c = "%" + ans3c + "%"

    if nicotine == "both":
        nicotine = "%"
    if gender == "Alla":
        gender = "%"

    query = """SELECT * FROM patients JOIN Studies ON key_id = Studies.patient JOIN Survays ON key_id = Survays.patient WHERE """
    query += " key_id ILIKE  '" + id + "'"
    query += " AND gender ILIKE  '" + gender + "'"
    query += " AND name ILIKE '" + name + "'"
    query += " AND CAST(weight AS TEXT) ILIKE  '" + weight + "'"
    query += " AND CAST(age AS TEXT) ILIKE  '" + age + "'"
    query += " AND CAST(studyNumber AS TEXT) ILIKE  '" + study + "'"
    query += " AND nicotine ILIKE '" + nicotine + "'"
    query += " AND (anwsers[0] ILIKE '" + ans1a + "' OR anwsers[0] ILIKE '" + ans2a + "' OR anwsers[0] ILIKE '" + ans3a + "')"
    query += " AND (anwsers[1] ILIKE '" + ans1b + "' OR anwsers[1] ILIKE '" + ans2b + "' OR anwsers[1] ILIKE '" + ans3b + "')"
    query += " AND (anwsers[2] ILIKE '" + ans1c + "' OR anwsers[2] ILIKE '" + ans2c + "' OR anwsers[2] ILIKE '" + ans3c + "')"
    

    print(query)
    return query + ";"

'''def buildQuery(id, gender, name, weight, age, nicotine, study):
    query = ""

    if name:
        name = "%" + name + "%"

    
    if len(study) == 0:
        query = """SELECT * FROM patients"""
    else:
        query ="""SELECT * FROM patients JOIN Studies ON key_id = patient"""

    if not (len(id) == 0 and gender == "Alla" and len(name) == 0 and len(weight) == 0 and len(age) == 0 and len(study) == 0):
        query += " WHERE"
        if not len(id) == 0:
            query += " key_id = '" + id + "'"
        if not gender == "Alla":
            if not "WHERE key_id" in query:
                query += " gender = '" + gender + "'"
            else:
                query += " AND gender = '" + gender + "'"
        if not len(name) == 0:
            if not ("WHERE key_id" in query or "gender" in query):
                query += " name ILIKE '" + name + "'"
            else:
                 query += " AND name ILIKE '" + name + "'"
        if not len(weight) == 0:
            if not ("WHERE key_id" in query or "gender" in query or "name" in query):
                query += " weight = '" + weight + "'"
            else:
                 query += " AND weight = '" + weight + "'"
        if not len(age) == 0:
            if not ("WHERE key_id" in query or "gender" in query or "name" in query or "weight" in query):
                query += " age = '" + age + "'"
            else:
                 query += " AND age = '" + age + "'"
        if not len(study) == 0:
            if not ("WHERE key_id" in query or "gender" in query or "name" in query or "weight" in query or "age" in query):
                query += " studyNumber = '" + study + "'"
            else:
                 query += " AND studyNumber = '" + study + "'"

    if nicotine == 'both':
        if 'WHERE' not in query:
            query += " WHERE"
            query += " nicotine LIKE '%'"
        else:
            query += " AND nicotine LIKE '%'"
    elif nicotine == 'Nej':
        if "WHERE" not in query:
            query += " WHERE"
        if not ("key_id" in query or "gender" in query or "name" in query or "weight" in query or "age" in query):
            query += " nicotine = 'Nej'"
        else:
            query += " AND nicotine = 'Nej'"
    elif nicotine == 'Ja':
        if "WHERE" not in query:
            query += " WHERE"
        if not ("key_id" in query or "gender" in query or "name" in query or "weight" in query or "age" in query):
            query += " nicotine = 'Ja'"
        else:
            query += " AND nicotine = 'Ja'"

    print(query)
    return query + ";"'''

# Unused for now
def runQuery(query):
    """
    This function runs the query in postgresql.
    """
    database = db.get_db()
    cur = database.cursor(cursor_factory=psycopg2.extras.DictCursor) # needed for select queries
    cur.execute(query)
    database.commit()
    res = cur.fetchall()
    return res
