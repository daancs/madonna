from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import psycopg2, psycopg2.extras

from flaskr.auth import login_required

from . import db

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
        print(request.form['key_id'])
        id = request.form['key_id']
        gender = request.form['gender']
        name = request.form['name']
        weight = request.form['weight']
        age = request.form['age']

        query = buildQuery(id, gender, name, weight, age)

        conn = db.get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(
            """SELECT *
            FROM patients
            WHERE key_id = %s""",
            (request.form['key_id'],)
        )

        result = cur.fetchone()
        print(result)
            # result = "Error: unable to fetch data"
            # g.isResString = True
    return render_template('/search/search.html', result=result)

def buildQuery(id, gender, name, weight, age):
    query = """SELECT * FROM patients"""

    if not (len(id) == 0 and len(gender) == 0 and len(name) == 0 and len(weight) == 0 and len(age) == 0):
        query += " WHERE"
        if not len(id) == 0:
            query += " key_id = " + id
        if not len(gender) == 0:
            if "key_id" not in query:
                query += " "

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
