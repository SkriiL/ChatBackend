from flask import Flask, render_template, request
from flask_socketio import SocketIO
import user
import friends
import friend_request

app = Flask(__name__)
sio = SocketIO(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@sio.on('connect')
def connect():
    print(request.sid + ' connected')


# --------------- USER -------------


@sio.on('sign-in')
def sign_in(str):
    res = user.sign_in(str)
    sio.emit('signed-in', res)


@sio.on('create-user')
def create_user(user_str):
    errors = user.create(user_str)
    sio.emit('created-user', errors)


@sio.on('get-all-users')
def get_all_users(str):
    users = user.get_all()
    sio.emit('all-users', users)


@sio.on('get-user-by-id')
def get_user_by_id(user_id):
    u = user.get_single_by_id(user_id)
    sio.emit('single-user', u)


@sio.on('verify-email')
def verify_email(user_id):
    user.verify_email(user_id)


# ------------------ FRIENDS -----------------


@sio.on('get-friends-for-user')
def get_friends_for_user(user_id):
    f = friends.get_all_for_user(user_id)
    sio.emit('friends-for-user', f)


@sio.on('delete-friend')
def delete_friend(friend_id):
    friends.delete(friend_id)


# --------------- FRIEND REQUESTS


@sio.on('send-friend-request')
def send_friend_request(users_str):
    req = friend_request.send_request(users_str)
    sio.emit('new-friend-request', req)


@sio.on('get-friend-requests-for-user')
def get_friend_requests_for_user(user_id):
    reqs = friend_request.get_all_for_user(user_id)
    sio.emit('friend-requests-for-user', reqs)


@sio.on('accept-friend-request')
def accept_friend_request(fr_id):
    friend_request.accept(fr_id)


@sio.on('reject-friend-request')
def reject_friend_request(fr_id):
    friend_request.reject(fr_id)


if __name__ == '__main__':
    print('Server started on http://0.0.0.0:56789')
    sio.run(app, host='0.0.0.0', port=56789)