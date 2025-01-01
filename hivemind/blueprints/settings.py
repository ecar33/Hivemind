from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from hivemind.forms import AvatarForm, LoginForm, ProfileForm, SignupForm
from hivemind.models import User
from hivemind.core.extensions import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    return

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    profile_form = ProfileForm()
    avatar_form = AvatarForm()
    if profile_form.validate_on_submit():
        new_name = profile_form.name.data
        new_username = profile_form.username.data
        
        exists = db.session.execute(db.select(User).where(User.name == new_username)).scalars().first()
        if exists and exists != current_user:
            flash("Username already taken!", "error")
            return redirect(url_for('.settings'))
        
        current_user.name = new_name
        current_user.username = new_username
        db.session.commit()
        flash('Profile updated!')
        return redirect(url_for('.settings'))
    
    return render_template('settings.html', profile_form=profile_form, avatar_form=avatar_form)
