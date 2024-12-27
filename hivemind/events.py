from flask import flash, session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from hivemind.core.extensions import socketio, db
from hivemind.models import ChatroomParticipant, User
from textwrap import wrap

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
            db.session.add(participant)
            db.session.commit()

            user_list = db.session.execute(db.select(User.name)
                        .join(ChatroomParticipant, User.id == ChatroomParticipant.user_id)
                        .where(ChatroomParticipant.chatroom_id == chatroom_id)).scalars().all()
            join_room(room)

            emit('status', {
                'msg': f'{session['name']} has joined!'
                }, to=room)
    
            emit('update_userlist', {
                'userlist': user_list
                }, to=room)

        except Exception as e:
            db.session.rollback()
            print(f'An error occured: {e}', flush=True)
    else:
        join_room(room)
        print(f'User {current_user.name} has opened another connection.', flush=True)

@socketio.on('disconnect', namespace='/hive')
def on_disconnect():
    print('Disconnect event detected', flush=True)
    room = session.get('room')
    chatroom_id = room
    leave_room(room)
    try:
        participant = db.session.execute(db.select(ChatroomParticipant)
                                        .where(ChatroomParticipant.chatroom_id == chatroom_id)
                                        .where(ChatroomParticipant.user_id == current_user.id)
                                        ).scalars().first()
        if participant:
            db.session.delete(participant)
            db.session.commit()
            user_list = db.session.execute(db.select(User.name)
                                           .join(ChatroomParticipant, User.id == ChatroomParticipant.user_id)
                                           .where(ChatroomParticipant.chatroom_id == chatroom_id)).scalars().all()
            emit('status', {
                'msg': f'{session['name']} has left.'
                }, to=room)
            emit('update_userlist', {
                'userlist': user_list 
                }, to=room)
            
        else:
            print('Participant doesnt exist!')
    except Exception as e:
        print(f'Something went wrong: {e}', flush=True)
    
@socketio.on('send_message', namespace='/hive')
def on_send_message(message):
    room = session.get('room')
    message_formatted = '\n'.join(wrap(message['content'].replace("\n", ""), 50))
    emit('message', {
        'user_id': message['user_id'],
        'name': message['name'],
        'content': message_formatted,
    }, to=room)

