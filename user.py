import sqlite3
import common
import email_service
import permissions


def list_to_user(user_list):
    user = {
        'id': user_list[0],
        'username': user_list[1],
        'password': user_list[2],
        'status': user_list[3],
        'permissions': permissions.get_single_by_id(user_list[4])
    }
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
    c.execute('SELECT * FROM users WHERE id=?', params)
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


def create(user_str, create=False):
    user = user_str.split(';')
    id = 0
    errors = [0]
    if not create:
        id = int(user[0])
        params = (id, user[1], user[2], user[3], user[4])
    else:
        id = common.max_id('users') + 1
        params = (id, user[0], user[1], 'new user', 2)
        errors = check_for_sign_up_errors(list_to_user((id, user[0], user[1], 'new user', 2)))
    if errors[0] != 0:
        return errors
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES(?,?,?,?,?)', params)
    conn.commit()
    conn.close()
    return [0]


def delete(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('DELETE FROM users WHERE id=?', params)
    conn.commit()
    conn.close()


def edit(user_str):
    user = user_str.split(';')
    delete(user[0])
    create(user_str)


def sign_in(user_str):
    user = user_str.split(";")
    target = get_single_by_username(user[0])
    if target is None:
        return None
    if target['password'] == user[1]:
        return target
    else:
        return None


def check_for_sign_up_errors(user):
    errors = []
    for u in get_all():
        if user['username'] == u['username'] and 1 not in errors:
            errors.append(1)
    if len(errors) == 0:
        errors.append(0)
    return errors