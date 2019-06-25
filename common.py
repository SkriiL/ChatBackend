import sqlite3


def max_id(table):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    cmd = 'SELECT * FROM ' + table
    c.execute(cmd)
    res = c.fetchall()
    max = 0
    for r in res:
        if r[0] > max:
            max = r[0]