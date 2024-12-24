from flask import Blueprint, flash, redirect, render_template, url_for
from hivemind.core.extensions import db
from hivemind.models import ChatMessage, Chatroom

hive_bp = Blueprint('hive', __name__, url_prefix='/hive')

@hive_bp.route('/<int:chatroom>', methods=['GET', 'POST'])
def hive(chatroom):
    chatroom = db.session.execute(db.select(Chatroom).where(Chatroom.id == chatroom)).scalars().first()
    if chatroom:
        chatroom_id = chatroom.id
        chat_messages = db.session.execute(db.select(ChatMessage).where(ChatMessage.chatroom_id == chatroom_id)).scalars().all()
        print(f'Chatroom is {chatroom_id} created at {chatroom.created_at}')
        return render_template('hive.html', chatroom_id=chatroom_id, chat_messages=chat_messages)
    else:
        flash("Chatroom doesn't exist!")
        return redirect(url_for('main.index'))