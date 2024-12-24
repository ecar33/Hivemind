from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField

class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[DataRequired()])
    room = IntegerField('Room', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')
