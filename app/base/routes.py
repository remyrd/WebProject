from flask import render_template, redirect, flash, url_for
from . import base
from .forms import LoginForm
from config import OPENID_PROVIDERS
from app.models import User,Contact
from app import db, login_manager
from flask_login import current_user, login_required, logout_user

providers = OPENID_PROVIDERS
@base.route('/')
def index():
	return render_template('base/index.html')

@base.route('/user/<username>')
@login_required
def user(username):
	#login redirects to this function, so contacts are mapped instantly after login
	map_current_user_contacts()	
	return render_template('base/user.html', requests = len(current_user.already_requestee_id), username=username, title = username, requestable_users=current_user.requestable_users, already_requester_id=current_user.already_requester_id, already_requestee_id = current_user.already_requestee_id, friends = current_user.friends)

@base.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
		return redirect('/')
	
	return render_template('login.html',form = form, title = 'Sign In',providers=providers)

@base.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

"""maps the rest of users to the current user's perspective
	takes ID of the users in the DB to make 5 lists
	"""
@base.before_request
def map_current_user_contacts():
	users = User.query.all()
	current_user.accepted_requesters = [] 
	current_user.accepted_requestees = [] 
	current_user.already_requestee_id = []
	current_user.already_requester_id = []
	current_user.requestable_users = []
	current_user.friends =[]
	#lists id of all current_user's friends
	accepted_requesters_models=Contact.query.filter_by(accepted=True, requestee_id=current_user.id).all()
	for model in accepted_requesters_models:
		current_user.accepted_requesters.append(model.requester_id)
	accepted_requestees_models=Contact.query.filter_by(accepted=True, requester_id=current_user.id).all()
	for model in accepted_requestees_models:
		current_user.accepted_requestees.append(model.requestee_id) 
	
	#retrieve the id of all the users who have tried to contact current_user
	already_requestee_id_models = Contact.query.filter_by(requestee_id = current_user.id, accepted=False).all()
	for model in already_requestee_id_models:
		current_user.already_requestee_id.append(model.requester_id)
	
	#retrieve id of all users current_user has tried to contact
	already_requester_id_models = Contact.query.filter_by(requester_id = current_user.id, accepted=False).all()
	for model in already_requester_id_models:
		current_user.already_requester_id.append(model.requestee_id)
	
	#generate the available ask for friends list
	for user in users:
		if user.id not in (current_user.already_requestee_id or current_user.accepted_requestees or current_user.accepted_requesters) and user != current_user:
			current_user.requestable_users.append(user)		
		if user.id in (current_user.accepted_requestees or current_user.accepted_requesters):
			current_user.friends.append(user)
			