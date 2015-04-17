#!/usr/bin/env python

import os
from app import create_app, db
from flask_socketio import SocketIO
#from app.models import User
#from gevent.wsgi import WSGIServer

app = create_app('production')

if __name__ == '__main__':
	socketio.run(app)
