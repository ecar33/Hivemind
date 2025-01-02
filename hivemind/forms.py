from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, IntegerField, PasswordField, StringField, SubmitField
from hivemind.core.extensions import avatars

class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class SignupForm(FlaskForm):
    name = StringField('Display Name', validators=[DataRequired(), Length(1,20, message="Display name must be between 1 and 20 characters")])
    username = StringField('Username', validators=[DataRequired(), Length(5,20, message="Username must be between 3 and 20 characters")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, message="Password must be at least 3 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Password confirmation is required."), 
        EqualTo('password', message="Passwords must match."),])
    submit = SubmitField('Signup')
    
class ProfileForm(FlaskForm):
    name = StringField('Display Name', validators=[DataRequired(), Length(1, 20, message="Display name must be between 1 and 20 characters")], render_kw={"placeholder": 'Enter a display name...'})
    username = StringField('Username Name', validators=[DataRequired(), Length(1, 20, message="Username name must be between 3 and 20 characters")], render_kw={"placeholder": 'Enter a username...'})
    submit = SubmitField('Update')
    
class AvatarForm(FlaskForm):
    avatar = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(avatars, 'Images only!')])
    submit = SubmitField('Submit')