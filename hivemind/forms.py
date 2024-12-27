from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField

class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    room = IntegerField('Room', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')