from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegisterRoom(Form):
	roomname = StringField('roomname', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	verify_password = PasswordField('verify_password', validators=[DataRequired()])
	submit = SubmitField('Register Rooom')

class SignInRoom(Form):
	roomname = StringField('roomname', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
