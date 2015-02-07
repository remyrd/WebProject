#application factory function

from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap=Bootstrap()
db = SQLAlchemy()
def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	
	bootstrap.init_app(app)
	from .blueprints import chat as chat_blueprint
	app.register_blueprint(chat_blueprint)
	db.init_app(app)
	return app

