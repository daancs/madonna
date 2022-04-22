

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import psycopg2, psycopg2.extras

from . import db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    This function renders the query page. 
    If it is a POST request it parses the query and tries to run it in postgresql.
    Otherwise it just renders the page.
    """
    result = None
    g.isResString = False
    if request.method == 'POST':
        query = request.form['query']
        try:
            result = runQuery(query)
        except:
            result = "Error: unable to fetch data"
            g.isResString = True
    return render_template('/search/search.html', result=result)


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
