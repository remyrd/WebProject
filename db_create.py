#!/usr/bin/env python
from manage import app
from migrate.versioning import api
#from config import DevelopmentConfig
from app import db, config
import os.path

configuration = config[os.getenv('FLASK_CONFIG') or 'default']

SQLALCHEMY_MIGRATE_REPO = configuration.SQLALCHEMY_MIGRATE_REPO
SQLALCHEMY_DATABASE_URI = configuration.SQLALCHEMY_DATABASE_URI

with app.app_context():
    db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))