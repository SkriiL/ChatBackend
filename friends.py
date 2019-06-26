import sqlite3
import common
import user


def list_to_friend(friend_list):
    user1 = user.get_single_by_id(friend_list[1])
    user2 = user.get_single_by_id(friend_list[2])
    friend = {'id': friend_list[0], 'user1': user1, 'user2': user2}
    return friend


def get_all():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM friends')
    res = c.fetchall()
    conn.close()
    return [list_to_friend(r) for r in res]


def get_all_for_user(userId):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (userId, userId, )
    c.execute('SELECT * FROM friends WHERE user1Id=? OR user2Id=?', params)
    res = c.fetchall()
    conn.close()
    return [list_to_friend(r) for r in res]


def delete(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('DELETE FROM friends WHERE id=?', params)
    conn.commit()
    conn.close()


def create(id, user1Id, user2Id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id, user1Id, user2Id,)
    c.execute('INSERT INTO friends VALUES(?,?,?)', params)
    conn.commit()
    conn.close()