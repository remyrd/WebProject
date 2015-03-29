from flask import render_template, redirect, flash, url_for
from . import base
from .forms import LoginForm
from config import OPENID_PROVIDERS
from app.models import User,Contact
from app import db
from flask_login import current_user

providers = OPENID_PROVIDERS
@base.route('/')
def index():
	return render_template('base/index.html')

@base.route('/user/<username>')
def user(username):
	users = User.query.all()
	not_friends = None
	#generate the available friends list
	for user in users:
		if current_user.id not in Contact.requester_id.query.filter_by(requestee_id=user.id) and current_user.id not in Contact.requestee_id.query.filter_by(requester_id=user.id):
			not_friends.apend(user)			
	return render_template('base/user.html', username=username, title = username, users=not_friends)

@base.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
		return redirect('/')
	
	return render_template('login.html',form = form, title = 'Sign In',providers=providers)

@base.route('/adduser/<id>', methods=['GET','POST'])
def adduser(id):
	new_contact = Contact(requester_id=current_user.id, requestee_id=id)
	db.session.add(new_contact)
	return redirect(url_for('.index'))

