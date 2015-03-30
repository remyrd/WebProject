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
	return render_template('base/user.html', username=username, title = username, users=current_user.requestable_users, already_requester_id=current_user.already_requester_id)

@base.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
		return redirect('/')
	
	return render_template('login.html',form = form, title = 'Sign In',providers=providers)

@base.route('/adduser/<id>', methods=['GET','POST'])
@login_required
def adduser(id):
	new_contact = Contact(requester_id=current_user.id, requestee_id=id)
	db.session.add(new_contact)
	db.session.commit()
	return redirect(url_for('.user', username = current_user.username))

@base.route('/requests')
@login_required
def requests():
	users = User.query.all()
	return render_template("base/requests.html", users=users, requests = len(current_user.already_requestee_id), already_requestee_id = current_user.already_requestee_id)

@base.route('/confirm/<id>', methods=['GET','POST'])
@login_required
def confirm(id):
	confirmation = Contact.query.filter_by(requester=id,requestee=current_user.id).first()
	if confirmation:
		confirmation.accepted=True
	db.session.update(confirmation)
	db.session.commit()
	return redirect(url_for('.index'))

@base.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('.index'))

"""maps the rest of users to the current user's perspective
	takes ID of the users in the DB to make 5 lists
	"""
def map_current_user_contacts():
	users = User.query.all()
	current_user.accepted_requesters = [] 
	current_user.accepted_requestees = [] 
	current_user.already_requestee_id = []
	current_user.already_requester_id = []
	current_user.requestable_users = []
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
	requestable_users = list()
	for user in users:
		if user.id not in (current_user.already_requestee_id or current_user.accepted_requestees or current_user.accepted_requesters) and user != current_user:
			current_user.requestable_users.append(user)		
