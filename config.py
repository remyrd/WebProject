import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'garbage'

class TestingConfig(Config):
	TESTING = True

class ProductionConfig:
	pass

config = {
	'development': DevelopmentConfig,
	'testing' : TestingConfig,
	'production' : ProductionConfig,
	'default' : DevelopmentConfig
	}



