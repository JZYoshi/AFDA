import sqlite3

def init_db(filename='descriptors.db'):
    conn = sqlite3.connect(filename)
    with open('schema.sql', 'r') as schema:
        conn.executescript(schema.read())
    conn.close()

def get_db(filename='descriptors.db'):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    return conn