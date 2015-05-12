import gevent
from . import chat
from flask import render_template, jsonify
from flask_login import current_user
from ..models import Room


#from app import socketio
#from flask.ext.socketio import emit, join_room, leave_room, close_room, disconnect

@chat.route('/test_chat/<room_id>')
def test_chat(room_id):
	room = Room.query.get(room_id)
	if room:
		return render_template('chat/test_chat.html', room = room)
	else:
		flash('invalid room')
		return redirect(url_for('base.index'))	



