from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_user

from hivemind.forms import LoginForm
from hivemind.models import User
from hivemind.core.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        user: User = db.session.execute(db.select(User).where(User.username == username)).scalars().first()

        try:
            if user.username == username and user.validate_password(password):
                chatroom_id = request.form.get('room').strip()

                login_user(user)
                
                # Set flask session attr name for current_user list
                session['name'] = user.name
                session['room'] = chatroom_id
                return redirect(url_for('hive.hive', chatroom_id=chatroom_id))
            else:
                flash('User doesnt exist or password is incorrect.', 'error')
                return redirect(url_for('main.index'))
            
        except Exception as e:
            flash(f'Login failed! Error: {e}', 'error')
            return redirect(url_for('main.index'))

    return render_template('index.html', form=form)