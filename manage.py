from gevent import monkey
monkey.patch_all()

from app import create_app, socketio
from flask import Flask, render_template, session, request

app = create_app('production')

if __name__ == '__main__':
	socketio.run(app)
