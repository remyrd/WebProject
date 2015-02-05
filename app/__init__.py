#application factory function

from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap

bootstrap=Bootstrap()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	
	bootstrap.init_app(app)
	from .blueprints import chat as chat_blueprint
	app.register_blueprint(chat_blueprint)

	return app

