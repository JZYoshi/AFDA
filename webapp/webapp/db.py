import sqlite3
import pandas as pd

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def db_to_pandas(filename='descriptors.db'):
    db = get_db()
    climb = pd.read_sql_query('SELECT * FROM climb',db).add_suffix('_climb')
    cruise = pd.read_sql_query('SELECT * FROM cruise',db).add_suffix('_cruise')
    descent = pd.read_sql_query('SELECT * FROM descent', db).add_suffix('_descent')
    info = pd.read_sql_query('SELECT * FROM general_info', db)

    df = info.merge(descent, left_on='flight_id',right_on='flight_id_descent').drop(columns='flight_id_descent')
    df = df.merge(cruise, left_on='flight_id',right_on='flight_id_cruise').drop(columns='flight_id_cruise')
    df = df.merge(climb, left_on='flight_id',right_on='flight_id_climb').drop(columns='flight_id_climb')
    return df