from gevent import monkey
monkey.patch_all()

from app import socketio
from . import chat
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@chat.route('/test_chat')
def test_chat():
    return render_template('test_chat.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response',
         {'data': message['data']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    emit('my response',
         {'data': message['data']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms)})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms)})


@socketio.on('close room', namespace='/test')
def close(message):
    
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.'},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    emit('my response',
         {'data': message['data']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    emit('my response',
         {'data': 'Disconnected!'})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')