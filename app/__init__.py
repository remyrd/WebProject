#application factory function

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
socketio = SocketIO()

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
	
	bootstrap.init_app(app)
	db.init_app(app)
	socketio.init_app(app)
	return app

