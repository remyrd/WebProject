from flask import render_template
from . import chat

@chat.route('/')
def index():
	return render_template('chat/index.html')

@chat.route('/user/<username>')
def user(username):
	return render_template('chat/user.html', username=username)


