import os
import click
import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    conn = get_db()
    cur = conn.cursor()
    # execute all init .sql files here such as tables etc when schema is done
    sqlfile = open('db/schema.sql', 'r')
    cur.execute(sqlfile.read())
    conn.commit()


def clear_db():
    """
    This function tries to clear the database and it if fails it rollbacks so that no data is lost.
    """
    conn = get_db()
    cur = conn.cursor()
    try:
        print("Attempting to clear database")
        cur.execute("DROP SCHEMA public CASCADE")
        cur.execute("CREATE SCHEMA public")
        cur.execute("GRANT ALL ON SCHEMA public TO postgres")
        conn.commit()
        print("Database cleared")
    except:
        print("Error: unable to drop schema, something failed")
        conn.rollback()

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
    clear_db()
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

