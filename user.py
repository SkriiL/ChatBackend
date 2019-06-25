import sqlite3
import common


def list_to_user(user_list):
    user = {'id': user_list[0], 'username': user_list[1], 'email': user_list[2], 'password': user_list[3]}
    return user


def get_single_by_username(username):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (username,)
    c.execute('SELECT * FROM users WHERE username=?', params)
    res = c.fetchone()
    conn.close()
    if res is None:
        return None
    return list_to_user(res)


def get_single_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('SELECT * FROM users WHERE id=?', id)
    res = c.fetchone()
    conn.close()
    if res is None:
        return None
    return list_to_user(res)


def get_all():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    res = c.fetchall()
    conn.close()
    return [list_to_user(r) for r in res]


def create(user_str):
    user = user_str.split(';')
    id = common.max_id('users')
    params = (id, user[0], user[1], user[2])
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES(?,?,?,?)', params)
    conn.commit()
    conn.close()


def sign_in(user_str):
    user = user_str.split(";")
    target = get_single_by_username(user[0])
    if target is None:
        return None
    if target['password'] == user[1]:
        return target
    else:
        return None
