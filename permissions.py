import sqlite3


def list_to_permission(perm_list):
    chat = perm_list[2] == 'True'
    friends = perm_list[3] == 'True'
    user = perm_list[4] == 'True'
    return {
        'id': perm_list[0],
        'name': perm_list[1],
        'chat': chat,
        'friends': friends,
        'user': user,
    }


def get_single_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (id,)
    c.execute('SELECT * FROM permissions WHERE id=?', params)
    res = c.fetchone()
    return list_to_permission(res)