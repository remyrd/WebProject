import gevent
from . import chat
from flask import render_template, jsonify
from flask_login import current_user


#from app import socketio
#from flask.ext.socketio import emit, join_room, leave_room, close_room, disconnect

@chat.route('/test_chat')
def test_chat():
    return render_template('chat/test_chat.html')


