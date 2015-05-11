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

@rooms.route('/join_room', methods=['POST', 'GET'])
def join_room():
	form = SignInRoom()
	room = Room.query.filter_by(roomname = form.roomname.data).first()
	if form.validate_on_submit():
		if room is None or not room.verify_password(form.password.data):
			flash('incorrect roomname or password')
			return redirect(url_for('.join_room'))
		if room in current_user.rooms:
			flash('you already belong to this room!')
			return redirect(url_for('join_room'))
		flash('joined room '+room.roomname+'\n you can now select it from the header')
		current_user.rooms.append(room)
		return redirect(url_for('base.index'))
	return render_template('rooms/join_room.html', form = form)

