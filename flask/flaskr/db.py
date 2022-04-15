import os
import click
import psycopg2
from flask import g
from flask.cli import with_appcontext

def init_app(app):
    app.teardown_appcontext(close_db)
    get_db()


def init_db():
    conn = get_db()
    cur = conn.cursor()
    # execute all init .sql files here such as tables etc when schema is done 
    sqlfile = open('flaskr/schema.sql', 'r')
    cur.execute(sqlfile.read())
    conn.commit()

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect( #conn = psycop...
                host="localhost",
                database="madonna",
                user="postgres",
                password="postgres"
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)