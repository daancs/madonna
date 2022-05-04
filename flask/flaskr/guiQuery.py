from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import psycopg2, psycopg2.extras

from flaskr.auth import login_required

from . import db
# from . import queryLogger

bp = Blueprint('search', __name__)

@bp.route('/search', methods=['GET', 'POST'])
#@login_required
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
        try:
            nicotine = request.form['nicotine']
        except:
            nicotine = False


        query = buildQuery(id, gender, name, weight, age, nicotine)

        db.addToHistory(g.user[1],query)

        conn = db.get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(query)

        result = cur.fetchone()
        print(result)
            # result = "Error: unable to fetch data"
            # g.isResString = True
    return render_template('/search/search.html', result=result)

def buildQuery(id, gender, name, weight, age, nicotine):
    query = """SELECT * FROM patients"""

    if not (len(id) == 0 and len(gender) == 0 and len(name) == 0 and len(weight) == 0 and len(age) == 0):
        query += " WHERE"
        if not len(id) == 0:
            query += " key_id = '" + id + "'"
        if not len(gender) == 0:
            if not "key_id" in query:
                query += " gender = '" + gender + "'"
            else:
                query += " AND gender = '" + gender + "'"
        if not len(name) == 0:
            if not ("key_id" in query or "gender" in query):
                query += " name = '" + name + "'"
            else:
                 query += " AND name = '" + name + "'"
        if not len(weight) == 0:
            if not ("key_id" in query or "gender" in query or "name" in query):
                query += " weight = '" + weight + "'"
            else:
                 query += " AND weight = '" + weight + "'"
        if not len(age) == 0:
            if not ("key_id" in query or "gender" in query or "name" in query or "weight" in query):
                query += " age = '" + age + "'"
            else:
                 query += " AND age = '" + age + "'"

    if not nicotine:
        if "WHERE" not in query:
            query += " WHERE"
        if not ("key_id" in query or "gender" in query or "name" in query or "weight" in query or "age" in query):
            query += " nicotine = 'Nej'"
        else:
            query += " AND nicotine = 'Nej'"
    else:
        if "WHERE" not in query:
            query += " WHERE"
        if not ("key_id" in query or "gender" in query or "name" in query or "weight" in query or "age" in query):
            query += " nicotine = 'Ja'"
        else:
            query += " AND nicotine = 'Ja'"

    print(query)
    return query + ";"

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
