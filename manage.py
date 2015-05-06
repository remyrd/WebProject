import gevent
import redis
import os
from gevent import monkey
monkey.patch_all()

from app import create_app
from flask import Flask
from flask.ext.sockets import Sockets



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
				app.logger.info(u'Sending message: {}'.format(data))
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

app = create_app('production')



sockets = Sockets(app)

chats = ChatBackend()
chats.start()
