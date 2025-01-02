from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user

from hivemind.forms import LoginForm, SignupForm
from hivemind.models import User
from hivemind.core.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        user: User = db.session.execute(db.select(User).where(User.username == username)).scalars().first()

        try:
            if user.username == username and user.validate_password(password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('User doesnt exist or password is incorrect.', 'error')
                return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'Login failed! Error: {e}', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        exists = db.session.execute(db.select(User).where(User.username == username)).scalars().first()
        
        if not exists:
            user = User(username=username, name=name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User successfully created! Please sign in.', 'success')        
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists, please use a different username.', 'error')     
            return redirect(url_for('auth.signup'))
        
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('auth.login'))
