import sqlite3
import common
import user
import friends


def list_to_friend_request(fr_list):
    user1 = user.get_single_by_id(fr_list[1])
    user2 = user.get_single_by_id(fr_list[2])
    friend_request = {'id': fr_list[0], 'user1': user1, 'user2': user2}
    return friend_request


def send_request(users_str):
    user_ids = users_str.split(';')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (common.max_id('friendRequests') + 1, user_ids[0], user_ids[1])
    c.execute('INSERT INTO friendRequests VALUES(?,?,?)', params)
    conn.commit()
    conn.close()
    return user_ids[1]


def get_all_for_user(user_id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (user_id,)
    c.execute('SELECT * FROM friendRequests WHERE user2Id=?', params)
    res = c.fetchall()
    conn.close()
    return [list_to_friend_request(r) for r in res]


def delete(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('DELETE FROM friendRequests WHERE id=?', params)
    conn.commit()
    conn.close()


def get_single_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('SELECT * FROM friendRequests WHERE id=?', params)
    res = c.fetchone()
    conn.close()
    return list_to_friend_request(res)


def accept(id):
    req = get_single_by_id(id)
    delete(id)
    friends.create(id, req['user1']['id'], req['user2']['id'])


def reject(id):
    delete(id)

