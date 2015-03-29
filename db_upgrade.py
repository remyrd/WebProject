#!/usr/bin/env python
from migrate.versioning import api
from app import config
import os.path

configuration = config[os.getenv('FLASK_CONFIG') or 'default']

SQLALCHEMY_MIGRATE_REPO = configuration.SQLALCHEMY_MIGRATE_REPO
SQLALCHEMY_DATABASE_URI = configuration.SQLALCHEMY_DATABASE_URI

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))