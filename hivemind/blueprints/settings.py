import os
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from hivemind.forms import AvatarForm, ProfileForm
from hivemind.models import User
from hivemind.core.extensions import db, avatars

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')
DEFAULT_AVATARS_PATH = 'avatars/default.jpg'

@settings_bp.route('/upload-avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    form = AvatarForm()
    
    if form.validate_on_submit():
        if current_user.profile_picture != DEFAULT_AVATARS_PATH:
            try:
                filepath = os.path.join(current_app.static_folder, current_user.profile_picture)
                os.remove(filepath)
            except OSError:
                flash("Filename doesn't exist!", 'error')
                
        filename = avatars.save(form.avatar.data, name=f'{current_user.id}.')
        print('avatars/' + filename, flush=True)
        current_user.set_profile_picture('avatars/' + filename)
        db.session.commit()
        
        flash('Avatar succesfully updated!')
        return redirect(url_for('settings.upload_avatar'))
    
    return render_template('settings/upload_avatar.html', form=form)
        

@settings_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile_form = ProfileForm()
    avatar_form = AvatarForm()
    if profile_form.validate_on_submit():
        new_name = profile_form.name.data
        new_username = profile_form.username.data
        
        exists = db.session.execute(db.select(User).where(User.name == new_username)).scalars().first()
        if exists and exists != current_user:
            flash("Username already taken!", "error")
            return redirect(url_for('.edit_profile'))
        
        current_user.name = new_name
        current_user.username = new_username
        db.session.commit()
        flash('Profile updated!')
        return redirect(url_for('.edit_profile'))
    
    return render_template('settings/edit_profile.html', profile_form=profile_form, avatar_form=avatar_form)
