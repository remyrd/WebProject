from . import rooms
from flask import redirect, render_template, url_for, flash
from app import db
from .forms import SignInRoom, RegisterRoom
from ..models import Room
from flask.ext.login import current_user


@rooms.route('/add_room', methods=['POST','GET'])
def add_room():
	form = RegisterRoom()
	if form.validate_on_submit():
		if form.password.data != form.verify_password.data:
			flash('passwords do not match!')
			return redirect(url_for('.add_room'))
		else:
			flash('room registered succesfully')
			room = Room(
						roomname=form.roomname.data, 
						password=form.password.data, 
						admin_id=current_user.id
						)
			db.session.add(room)
			db.session.commit()
			return redirect(url_for('chat.test_chat'))
	return render_template('rooms/add_room.html',form=form)

#@rooms.route('/join_room/<roomname>')

