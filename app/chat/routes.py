from . import chat
from flask import render_template, redirect, url_for, flash
from ..models import *
from flask_login import current_user, login_required
from app import socketio
from flask_socketio import emit

@chat.route('/test_chat')
def test_chat():
	return render_template('chat/test_chat.html')

@socketio.on('a message')
def echo(message):
	emit('response from server', {'data': message['data']})

@socketio.on('connect')
def test_connect():
	emit('connect')

