import sqlite3
import pandas as pd

def init_db(filename='../data/descriptors.db'):
    """
    Execute the script schema.sql to initialize the sqlite database.

    :param filename: the name of the output sqlite database
    """
    conn = sqlite3.connect(filename)
    with open('schema.sql', 'r') as schema:
        conn.executescript(schema.read())
    conn.close()

def get_db(filename='../data/descriptors.db'):
    """
    Return a connection object corresponding to the specified filename.

    :param filename:
    """
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn

def db_to_pandas(filename='../data/descriptors.db'):
    """
    Convert the sql database containing descriptors to a pandas dataframe.

    :param filename: the name of the database containing the descriptors.
    :returns: a dataframe containing every descriptors of each flight
    """
    db = get_db(filename)
    climb = pd.read_sql_query('SELECT * FROM climb',db).add_suffix('_climb')
    cruise = pd.read_sql_query('SELECT * FROM cruise',db).add_suffix('_cruise')
    descent = pd.read_sql_query('SELECT * FROM descent', db).add_suffix('_descent')
    info = pd.read_sql_query('SELECT * FROM general_info', db)

    df = info.merge(descent, left_on='flight_id',right_on='flight_id_descent').drop(columns='flight_id_descent')
    df = df.merge(cruise, left_on='flight_id',right_on='flight_id_cruise').drop(columns='flight_id_cruise')
    df = df.merge(climb, left_on='flight_id',right_on='flight_id_climb').drop(columns='flight_id_climb')
    return df