import os
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db_conn():
    if 'db' not in g:
        g.db = psycopg2.connect( #conn = psycop...
                host="localhost",
                database="madonna",
                user=os.environ['DB_USERNAME'],
                password=os.environ['DB_PASSWORD'])

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    conn = get_db_conn()
    cur = conn.cursor()

    with current_app.open_resource('schema.sql') as f:
        cur.execute(f.read())
        conn.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
