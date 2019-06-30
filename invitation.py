import common
import sqlite3


def get_single_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('SELECT * FROM invitations WHERE id=?', params)
    res = c.fetchone()
    return {'id': int(res[0]), 'activated': res[1] == 'True'}


def invite():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    id = common.max_id('invitations') + 1
    params = (id, 'False')
    c.execute('INSERT INTO invitations VALUES(?,?)', params)
    conn.commit()
    conn.close()
    return 'localhost:4200/invitation/' + str(id)


def delete(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('DELETE FROM invitations WHERE id=?', params)
    conn.commit()
    conn.close()


def activate(id):
    i = get_single_by_id(id)
    if not i['activated']:
        delete(id)
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        params = (id, 'True')
        c.execute('INSERT INTO invitations VALUES(?,?)', params)
        conn.commit()
        conn.close()
        return True
    else:
        return False
