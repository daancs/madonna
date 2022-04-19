from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import psycopg2, psycopg2.extras

from . import db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET', 'POST'])
def index():
    result = None
    g.isResString = False
    if request.method == 'POST':
        query = request.form['query']
        try:
            result = runQuery(query)
        except:
            result = "Error: unable to fetch data"
            g.isResString = True
    return render_template('/search/index.html', result=result)


def runQuery(query):
    database = db.get_db()
    cur = database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    database.commit()
    res = cur.fetchall()
    first = res[0]
    print(first.items())
    print(type(first))
    print(res[0]['id'])
    return res
