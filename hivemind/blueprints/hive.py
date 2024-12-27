from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import login_required
from hivemind.core.extensions import db
from hivemind.models import ChatMessage, Chatroom, ChatroomParticipant, User

hive_bp = Blueprint('hive', __name__, url_prefix='/hive')

@hive_bp.route('/<int:chatroom_id>')
@login_required
def hive(chatroom_id):
    chatroom = db.session.execute(db.select(Chatroom).where(Chatroom.id == chatroom_id)).scalars().first()
    if chatroom:
        participants = db.session.execute(db.select(User.name)
                                           .join(ChatroomParticipant, User.id == ChatroomParticipant.user_id)
                                           .where(ChatroomParticipant.chatroom_id == chatroom_id)).scalars().all()
        chat_messages = db.session.execute(db.select(ChatMessage).where(ChatMessage.chatroom_id == chatroom_id)).scalars().all()
        return render_template('hive.html', chatroom_id=chatroom_id, chat_messages=chat_messages, participants=participants)
    else:
        flash("Chatroom doesn't exist!", 'error')
        return redirect(url_for('main.index'))