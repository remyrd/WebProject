#!/usr/bin/env python
from manage import app
from app import db
from app.models import User
from getpass import getpass


password = getpass()
password2= getpass()
if password2 != password:
	import sys
	sys.exit("passwords don\'t match")
new_user=User(username=argv[1], email= argv[1]+"@pwebproject.org", password=password)
db.session.add(new_user)
db.session.commit()