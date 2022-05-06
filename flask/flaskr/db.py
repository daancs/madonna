import os
import click
import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext

from werkzeug.security import generate_password_hash

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
                password=os.environ['DB_PASSWORD']
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def addToHistory(user, query):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("INSERT INTO SearchHistory (who, query) VALUES (%s,%s)",(user,query))
    conn.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    clear_db()
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(registerAccount)


@click.command('register')
@with_appcontext
@click.argument('username')
@click.argument('password')
def registerAccount(username, password):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, generate_password_hash(password))) # här skriver man sina inloggningsuppg om man vill skapa en ny. kanske fixa ett bättre sätt???
    conn.commit()
    click.echo("Account created")


#############  DEN KOMMENTERADE KODEN OVAN GÖR ATT MAN KAN GÖRA EN ANVÄNDARE FÖR APPLIKATIONEN ########################
