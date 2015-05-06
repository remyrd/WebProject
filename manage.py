import gevent

from gevent import monkey
monkey.patch_all()

from app import create_app
from flask import Flask
from flask.ext.sockets import Sockets


app = create_app('production')
sockets = Sockets(app)

