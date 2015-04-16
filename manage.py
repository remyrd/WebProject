#!/usr/bin/env python

import os
from app import create_app, db
from flask_script import Manager
from app.models import User


app = create_app('production')

manager = Manager(app)

@manager.command
def adduser(username):
	from getpass import getpass
	password = getpass()
	password2 = getpass()
	if password != password2:
		import sys
		sys.exit("passwords do not match")
	user = User(email = username+"@haha.com", username = username, password = password)
	db.session.add(user)
	db.session.commit()
	

if __name__ == '__main__':
	manager.run()

