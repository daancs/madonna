import os
import psycopg2

def init_app(app):
    app.teardown_appcontext(close_db)
    get_db()

def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="portal",
        user="postgres",
        password="postgres"
    )

    return conn.cursor()

def close_db():
    conn.close()
