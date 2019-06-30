from flask import Flask, render_template, request
from flask_socketio import SocketIO
import user
import friends
import friend_request
import chat
import message
import invitation

app = Flask(__name__)
sio = SocketIO(app)


sids = {}


@app.route('/')
def index():
    return app.send_static_file('index.html')


@sio.on('connect')
def connect():
    sio.emit('connected', request.sid)
    print(request.sid + ' connected')


# --------------- USER -------------


@sio.on('sign-in')
def sign_in(str, sid):
    res = user.sign_in(str)
    sio.emit('signed-in', res, room=sid['_value'])
    if res is not None:
        sids[res['id']] = sid['_value']


@sio.on('create-user')
def create_user(user_str, sid):
    errors = user.create(user_str, True)
    sio.emit('created-user', errors)


@sio.on('get-all-users')
def get_all_users(str, sid):
    users = user.get_all()
    sio.emit('all-users', users)


@sio.on('get-user-by-id')
def get_user_by_id(user_id, sid):
    u = user.get_single_by_id(user_id)
    sio.emit('single-user', u)


# ------------------ FRIENDS -----------------


@sio.on('get-friends-for-user')
def get_friends_for_user(user_id, sid):
    f = friends.get_all_for_user(user_id)
    sio.emit('friends-for-user', f)


@sio.on('delete-friend')
def delete_friend(friend_id, sid):
    friends.delete(friend_id)


# --------------- FRIEND REQUESTS


@sio.on('send-friend-request')
def send_friend_request(users_str, sid):
    req = friend_request.send_request(users_str)
    sio.emit('new-friend-request', req)


@sio.on('get-friend-requests-for-user')
def get_friend_requests_for_user(user_id, sid):
    reqs = friend_request.get_all_for_user(user_id)
    sio.emit('friend-requests-for-user', reqs)


@sio.on('accept-friend-request')
def accept_friend_request(fr_id, sid):
    friend_request.accept(fr_id)


@sio.on('reject-friend-request')
def reject_friend_request(fr_id, sid):
    friend_request.reject(fr_id)


# --------------- CHATS -------------


@sio.on('get-chats-for-user')
def get_chats_for_user(user_id, sid):
    chats = chat.get_all_for_user(user_id)
    sio.emit('chats-for-user', chats)


@sio.on('get-chat-between-users')
def get_chat_between_users(users, sid):
    c = chat.get_between_users(users)
    sio.emit('chat', c, room=sid['_value'])


@sio.on('create-chat')
def create_chat(users, sid):
    id = chat.create(users)
    sio.emit('created-chat', id, room=sid['_value'])


@sio.on('get-single-chat')
def get_single_chat(chat_id, sid):
    c = chat.get_single_by_id(chat_id)
    sio.emit('single-chat', c)


@sio.on('invite')
def invite(arg, sid):
    link = invitation.invite()
    sio.emit('invitation', link)


@sio.on('activate-invitation')
def activate_invitation(id, sid):
    res = invitation.activate(id)
    sio.emit('activated-invitation', res)


# ---------------- MESSAGES ------------


@sio.on('get-messages-sorted-for-chat')
def get_messages_for_chat(chat_id, sid):
    messages = message.get_all_sorted_for_chat(chat_id)
    sio.emit('messages-sorted-for-chat-' + chat_id, messages)


@sio.on('send-message')
def send_message(message_str, sid):
    user_id = message.send_message(message_str)
    sio.emit('new-message', 'new')



if __name__ == '__main__':
    print('Server started on http://0.0.0.0:56789')
    sio.run(app, host='0.0.0.0', port=56789)