#!/usr/bin/env python
from migrate.versioning import api
from app import config

configuration = config['production']

SQLALCHEMY_MIGRATE_REPO = configuration.SQLALCHEMY_MIGRATE_REPO
SQLALCHEMY_DATABASE_URI = configuration.SQLALCHEMY_DATABASE_URI

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))