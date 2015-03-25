#application factory function

from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


bootstrap=Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view ='auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	login_manager.init_app(app)
	
	bootstrap.init_app(app)
	
	from .base import base as base_blueprint
	app.register_blueprint(base_blueprint)
	
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	
	db.init_app(app)
	return app

