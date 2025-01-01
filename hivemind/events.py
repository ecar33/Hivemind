from flask import flash, session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from hivemind.core.extensions import socketio, db
from hivemind.models import ChatroomParticipant
from textwrap import wrap

connections = {}

@socketio.on('join', namespace='/hive')
def on_join():
    room = session.get('room')
    chatroom_id = room
    exists = db.session.execute(db.select(ChatroomParticipant)
                                .where(ChatroomParticipant.user_id == current_user.id)
                                .where(ChatroomParticipant.chatroom_id == chatroom_id)).scalars().first()
    if not exists:
        try:
            participant = ChatroomParticipant(chatroom_id=chatroom_id, user_id=current_user.id)
            connections[current_user.id] = connections.get(current_user.id, 0) + 1

            db.session.add(participant)
            db.session.commit()

            join_room(room)

            emit('status', {
                'msg': f'{current_user.name} has joined!'
                }, to=room)
    
            emit('add_to_userlist', {
                'new_user': current_user.to_dict()
                }, to=room)

        except Exception as e:
            db.session.rollback()
            print(f'An error occured: {e}', flush=True)
    else:
        join_room(room)
        connections[current_user.id] = connections.get(current_user.id, 0) + 1
        print(f'User {current_user.name} has opened another connection.', flush=True)

@socketio.on('disconnect', namespace='/hive')
def on_disconnect():
    room = session.get('room')
    chatroom_id = room

    # Check connections for the current user
    if connections.get(current_user.id, 0) > 1:
        connections[current_user.id] -= 1
        print(f"Connection decremented for {current_user.name}", flush=True)
        return
    else:
        # Handle last connection
        connections.pop(current_user.id, None)
        leave_room(room)
        try:
            participant = db.session.execute(
                db.select(ChatroomParticipant)
                  .where(ChatroomParticipant.chatroom_id == chatroom_id)
                  .where(ChatroomParticipant.user_id == current_user.id)
            ).scalars().first()
            
            if participant:
                db.session.delete(participant)
                db.session.commit()
                
                # Notify other users
                emit('status', {
                    'msg': f'{current_user.name} has left.'
                }, to=room)
                
                emit('remove_from_userlist', {
                    'user_to_delete': current_user.id
                }, to=room)
            else:
                print('Participant does not exist!')
        except Exception as e:
            print(f'Something went wrong: {e}', flush=True)
        finally:
            leave_room(room)
    
@socketio.on('send_message', namespace='/hive')
def on_send_message(message):
    room = session.get('room')
    message_formatted = '\n'.join(wrap(message['content'].replace("\n", ""), 50))
    emit('message', {
        'user_id': message['user_id'],
        'name': message['name'],
        'content': message_formatted,
    }, to=room)

