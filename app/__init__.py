#application factory function

import os
import redis
import gevent
from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO


bootstrap=Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view ='auth.login'



REDIS_URL = os.environ['REDISCLOUD_URL']
REDIS_CHAN = 'chat'

redis = redis.from_url(REDIS_URL)

class ChatBackend(object):
	def __init__(self):
		self.clients = list()
		self.pubsub = redis.pubsub()
		self.pubsub.subscribe(REDIS_CHAN)

	def __iter_data(self):
		for message in self.pubsub.listen():
			data = message.get('data')
			if message['type'] == 'message':
				#app.logger.info(u'Sending message: {}'.format(data))
				yield data

	def register(self, client):
		"""Register a Websocket connection for Redis updates"""
		self.clients.append(client)

	def send(self,client,data):
		"""Send given data to registered client. Automatically discards invalid connections"""
		try:
			client.send(data)
		except Exception:
			self.clients.remove(client)

	def run(self):
		"""Listens for new messages in Redis, and sends them to clients"""
		for data in self.__iter_data():
			for client in self.clients:
				gevent.spawn(self.send, client, data)

	def start(self):
		"""Maintains Redis subscription in the background"""
		gevent.spawn(self.run)

chats = ChatBackend()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	login_manager.init_app(app)
	app.debug = True

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
	chats.start()
	
	return app

