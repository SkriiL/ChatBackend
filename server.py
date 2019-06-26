from flask import Flask, render_template, request
from flask_socketio import SocketIO
import user

app = Flask(__name__)
sio = SocketIO(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@sio.on('connect')
def connect():
    print(request.sid + ' connected')


@sio.on('sign-in')
def sign_in(str):
    res = user.sign_in(str)
    signed_in(res)


def signed_in(user):
    sio.emit('signed-in', user)


@sio.on('create-user')
def create_user(user_str):
    errors = user.create(user_str)
    created_user(errors)


def created_user(errors):
    sio.emit('created-user', errors)


@sio.on('verify-email')
def verify_email(user_id):
    user.verify_email(user_id)


if __name__ == '__main__':
    print('Server started on http://0.0.0.0:56789')
    sio.run(app, host='0.0.0.0', port=56789)