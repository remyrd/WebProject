#application factory function

import os
import redis
from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from .chat_backend import ChatBackend

bootstrap=Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view ='auth.login'
socketio = SocketIO()
chat = ChatBackend()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	login_manager.init_app(app)
	app.debug = 'DEBUG' in os.environ

	from .base import base as base_blueprint
	app.register_blueprint(base_blueprint)
	
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	
	from .contacts import contacts as contacts_blueprint
	app.register_blueprint(contacts_blueprint, url_prefix='/contacts')

	from .chat import chat as chat_blueprint
	app.register_blueprint(chat_blueprint, url_prefix='/chat')

	from .rooms import rooms as rooms_blueprint
	app.register_blueprint(rooms_blueprint, url_prefix='/rooms')
	
	bootstrap.init_app(app)
	db.init_app(app)
	socketio.init_app(app)
	redis = redis.from_url(REDIS_URL)
	chat.start()
	
	return app

