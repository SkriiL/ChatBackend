import sqlite3
import common
import date
import user
import chat


def list_to_message(message_list):
    u = user.get_single_by_id(message_list[1])
    d = date.db_to_date(message_list[2])
    c = chat.get_single_by_id(message_list[3])
    return {'id': message_list[0], 'user': u, 'date': d, 'chat': c, 'content': message_list[4]}


def get_all_sorted_for_chat(chat_id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (chat_id,)
    c.execute('SELECT * FROM messages WHERE chatId=?', params)
    res = c.fetchall()
    messages = [list_to_message(r) for r in res]
    return sort_by_date(messages)


def send_message(message_str):
    message = message_str.split(';')
    params = (common.max_id('messages') + 1, message[0], message[1], message[2], message[3])
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages VALUES(?,?,?,?,?)', params)
    conn.commit()
    conn.close()
    c = chat.get_single_by_id(int(message[2]))
    if c['user1']['id'] == int(message[0]):
        return c['user2']['id']
    return c['user1']['id']


def sort_by_date(messages):
    new = []
    last_day = 0
    last_month = 0
    last_year = 0
    index = 0
    for m in messages:
        if last_day == 0:
            new.append([m])
        elif m['date']['day'] > last_day and m['date']['month'] == last_month and m['date']['year'] == last_year:
            new.append([m])
            index += 1
        elif m['date']['month'] > last_month and m['date']['year'] == last_year:
            new.append([m])
            index += 1
        elif m['date']['year'] > last_year:
            new.append([m])
            index += 1
        elif m['date']['day'] == last_day and m['date']['month'] == last_month and m['date']['year'] == last_year:
            new[index].append(m)

        last_day = m['date']['day']
        last_month = m['date']['month']
        last_year = m['date']['year']
    return new