import os
import click
import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext

def init_db():
    conn = get_db()
    cur = conn.cursor()

    with current_app.open_resource('../db/schema.sql') as f:
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

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host="localhost",
            database="madonna",
            #user=os.environ['DB_USERNAME'],
            #password=os.environ['DB_PASSWORD'])
            user="postgres",
            password="Simonsson01")
        '''
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
            current_app.config['DATABASE'],
            #Oklart vad man ska skriva för att detecta types i psycopg2
            detect_types=sqlite3.PARSE_DECLTYPES
        '''
        #g.db.row_factory = psycopg2.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



'''def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="portal",
        user="postgres",
        password="postgres"
    )

    return conn.cursor()

def close_db():
    conn.close()
'''
