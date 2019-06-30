import sqlite3
import common
import user


def list_to_chat(chat_list):
    user1 = user.get_single_by_id(chat_list[1])
    user2 = user.get_single_by_id(chat_list[2])
    chat = {'id': chat_list[0], 'user1': user1, 'user2': user2}
    return chat


def get_all_for_user(user_id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (user_id, user_id,)
    c.execute('SELECT * FROM chats WHERE user1Id=? OR user2Id=?', params)
    res = c.fetchall()
    return [list_to_chat(r) for r in res]


def get_single_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('SELECT * FROM chats WHERE id=?', params)
    res = c.fetchone()
    return list_to_chat(res)


def create(users_str):
    id = common.max_id('chats') + 1
    users = users_str.split(';')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id, users[0], users[1],)
    c.execute('INSERT INTO chats VALUES(?,?,?)', params)
    conn.commit()
    conn.close()
    return id


def get_between_users(users_str):
    users = users_str.split(';')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (users[0], users[1],)
    c.execute('SELECT * FROM chats WHERE user1Id=? AND user2Id=?', params)
    res1 = c.fetchone()
    c.execute('SELECT * FROM chats WHERE user2Id=? AND user1Id=?', params)
    res2 = c.fetchone()
    conn.close()
    if res1 is not None:
        return list_to_chat(res1)
    elif res2 is not None:
        return list_to_chat(res2)
    else:
        return 'None'
