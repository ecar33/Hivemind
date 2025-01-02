from flask import session, url_for
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from hivemind.core.extensions import socketio, db
from hivemind.models import ChatroomParticipant
from textwrap import wrap

connections = {}

@socketio.on('join', namespace='/hive')
def on_join(data):
    room = data['room']
    session['room'] = room
    chatroom_id = room

    exists = db.session.execute(
        db.select(ChatroomParticipant)
        .where(ChatroomParticipant.user_id == current_user.id)
        .where(ChatroomParticipant.chatroom_id == chatroom_id)
    ).scalars().first()

    if not exists:
        try:
            participant = ChatroomParticipant(chatroom_id=chatroom_id, user_id=current_user.id)
            connections[current_user.id] = connections.get(current_user.id, 0) + 1

            db.session.add(participant)
            db.session.commit()

            join_room(room)

            emit('status', {'msg': f'{current_user.name} has joined!'}, to=room)
            emit('add_to_userlist', {
                'new_user': current_user.to_dict(),
                'avatar': url_for('static', filename=current_user.profile_picture)
            }, to=room)

        except Exception as e:
            db.session.rollback()
            print(f'An error occurred: {e}', flush=True)
    else:
        join_room(room)
        connections[current_user.id] = connections.get(current_user.id, 0) + 1
        print(f'User {current_user.name} has opened another connection.', flush=True)


@socketio.on('disconnect', namespace='/hive')
def on_disconnect():
    room = session['room']
    chatroom_id = room

    if connections.get(current_user.id, 0) > 1:
        connections[current_user.id] -= 1
        print(f"Connection decremented for {current_user.name}. Remaining connections: {connections[current_user.id]}", flush=True)
        return

    connections.pop(current_user.id, None)
    leave_room(room)
    room = session.pop('room', None)

    try:
        participant = db.session.execute(
            db.select(ChatroomParticipant)
            .where(ChatroomParticipant.chatroom_id == chatroom_id)
            .where(ChatroomParticipant.user_id == current_user.id)
        ).scalars().first()

        if participant:
            db.session.delete(participant)
            db.session.commit()

            emit('status', {'msg': f'{current_user.name} has left.'}, to=room)
            emit('remove_from_userlist', {'user_to_delete': current_user.id}, to=room)
        else:
            print('Participant does not exist!', flush=True)

    except Exception as e:
        print(f'Something went wrong: {e}', flush=True)


@socketio.on('send_message', namespace='/hive')
def on_send_message(data):
    room = session.get('room', None)
    if room is None:
        print(f"User {current_user.name} attempted to send a message without being in a room.", flush=True)
        return

    message_formatted = '\n'.join(wrap(data['content'].replace("\n", ""), 50))
    emit('message', {
        'user_id': data['user_id'],
        'name': data['name'],
        'avatar': data['avatar'],
        'content': message_formatted,
    }, to=room)

