from flask import Blueprint, flash, redirect, render_template, request, url_for

from hivemind.forms import LoginForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        chatroom_id = request.form.get('room').strip()
        return redirect(url_for('hive.hive', chatroom_id=chatroom_id))
    return render_template('index.html', form=form)

@main_bp.route('/drawer', methods=['GET', 'POST'])
def test_drawer():
    return render_template('drawer.html')