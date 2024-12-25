from flask import session
from flask_socketio import emit, join_room
from hivemind.core.extensions import socketio


print("Registering 'join' event handler...")

@socketio.on('join', namespace='/hive')
def on_join(data):
    room = session.get('room')
    join_room(room)
    emit('ping', {
        'msg': 'You successfully connected!'
        }, to=room)

@socketio.on('send_message', namespace='/hive')
def on_send_message(message):
    room = session.get('room')
    emit('message', {
        'msg': f"<div> {session.get('name')}: {message['msg']} </div>",
    }, to=room)

