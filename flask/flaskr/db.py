import os
import click
import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime

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


def addToSearchHistory(user, id, gender, name, weight, age, nicotine, study,
                            ans1a, ans1b, ans1c,
                            ans2a, ans2b, ans2c,
                            ans3a, ans3b, ans3c):
    entry = entryBuilder(user, id, gender, name, weight, age, nicotine, study, ans1a, ans1b, ans1c,
                            ans2a, ans2b, ans2c,
                            ans3a, ans3b, ans3c)
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("INSERT INTO SearchHistory(search) VALUES ('" + entry + "')")
    conn.commit()

def entryBuilder(user, id, gender, name, weight, age, nicotine, study,
                            ans1a, ans1b, ans1c,
                            ans2a, ans2b, ans2c,
                            ans3a, ans3b, ans3c):
    now = datetime.now()
    entry = now.strftime("%d/%m/%Y %H:%M:%S") + ": " + str(user) + " sökte på alla patienter"

    if (len(id) != 0 or gender != "Alla" or len(name) != 0 or len(weight) != 0 or len(age) != 0 or len(study) != 0 or nicotine != "both"):
        entry += " som "

        if len(id) != 0:
            entry += " har id-nummer " + id + ", "

        if gender != "Alla":
            entry += " är av könet " + gender + ", "

        if len(name) != 0:
            entry += " heter " + name + ", "

        if len(weight) != 0:
            entry += " väger " + weight + " kg, "

        if len(age) != 0:
            entry += " är " + age + " år gamla, "

        if len(study) != 0:
            entry += " deltar i studie nummer " + study + ", "

    #if nicotine == "both":
    #    entry += "och är antingen rökare och ickerökare"
        if nicotine == "Nej":
            entry += "inte röker"
        if nicotine == "Ja":
            entry += "röker"

    if len(ans1a) > 0 or len(ans1b) > 0 or len(ans1c) > 0 or len(ans2a) > 0 or len(ans2b) > 0 or len(ans2c) > 0 or len(ans3a) > 0 or len(ans3b) > 0 or len(ans3c) > 0:
        if "som" not in entry:
            entry += " som har gett enkätsvaren: "
        else :
            entry += " och har gett enkätsvaren: "
        if len(ans1a) != 0:
            entry += ans1a + ", "
        if len(ans1b) != 0:
            entry += ans1b + ", "
        if len(ans1c) != 0:
            entry += ans1c + ", "
        if len(ans2a) != 0:
            entry += ans2a + ", "
        if len(ans2b) != 0:
            entry += ans2b + ", "
        if len(ans2c) != 0:
            entry += ans2c + ", "
        if len(ans3a) != 0:
            entry += ans3a + ", "
        if len(ans3b) != 0:
            entry += ans3b + ", "
        if len(ans3c) != 0:
            entry += ans3c
    

    if entry[-2] == ",":
        entry = entry[:-2]

    return entry

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
    app.cli.add_command(exportTable)


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

@click.command('export')
@with_appcontext
@click.argument('table')
def exportTable(table):
    conn = get_db()
    cur = conn.cursor()
    path = os.path.dirname(__file__)
    path = path + '\..\export\{}.csv'.format(table)
    query = "COPY {} TO STDOUT DELIMITER ',' CSV HEADER".format(table)
    try:
        f = open(path, 'w')
        cur.copy_expert(query, f)
        conn.commit()
    except:
        print("Error: unable to export table")
        conn.rollback()
        return
    click.echo("Table exported")
