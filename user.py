import sqlite3
import common
import email_service


def list_to_user(user_list):
    user = {'id': user_list[0], 'username': user_list[1], 'email': user_list[2], 'password': user_list[3], 'verified': user_list[4]}
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


def create(user_str, send_verification=True):
    user = user_str.split(';')
    id = 0
    if send_verification:
        verified = 'False'
    else:
        verified = user[4]
    try:
        id = int(user[0])
        params = (id, user[1], user[2], user[3], verified)
    except ValueError:
        id = common.max_id('users') + 1
        params = (id, user[0], user[1], user[2], verified)
    if send_verification:
        errors = check_for_sign_up_errors(list_to_user([id, user[0], user[1], user[2], False]))
        if 1 in errors or 2 in errors or 3 in errors:
            return errors
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES(?,?,?,?, ?)', params)
    conn.commit()
    conn.close()
    if send_verification:
        email_service.send_verification(list_to_user([id, user[0], user[1], user[2], False]))
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
    create(user_str, False)


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
        if user['email'] == u['email'] and 2 not in errors:
            errors.append(2)
        if user['username'] == u['username'] and 1 not in errors:
            errors.append(1)
        if not email_service.valid_email(user['email']) and 3 not in errors:
            errors.append(3)
    if len(errors) == 0:
        errors.append(0)
    return errors


def verify_email(id):
    user = get_single_by_id(id)
    user_str = str(user['id']) + ';' + user['username'] + ';' + user['email'] + ';' + user['password'] + ";True"
    edit(user_str)
