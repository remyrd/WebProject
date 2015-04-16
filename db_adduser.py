#!/usr/bin/env python
from manage import app
from app import db
from app.models import User
from getpass import getpass
import sys

password = getpass()
password2= getpass()
if password2 != password:
	sys.exit("passwords don\'t match")
new_user=User(username=sys.argv[1], email= sys.argv[1]+"@pwebproject.org", password=password)
db.session.add(new_user)
db.session.commit()