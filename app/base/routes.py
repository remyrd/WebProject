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
	accepted_requesters = [] 
	accepted_requestees = [] 
	already_requestee_id = []
	already_requester_id = []
	#lists id of all current_user's friends
	accepted_requesters.append(Contact.query.filter(Contact.accepted==True, Contact.requestee_id==current_user.id).value(Contact.requester_id))
	accepted_requestees.append(Contact.query.filter(Contact.accepted==True, Contact.requester_id==current_user.id).value(Contact.requestee_id)) 
	#retrieve the id of all the users who have tried to contact current_user
	already_requestee_id.append(Contact.query.filter(Contact.requestee_id == current_user.id, Contact.accepted==False).value(Contact.requester_id))
	#retrieve id of all users current_user has tried to contact
	already_requester_id.append(Contact.query.filter(Contact.requester_id == current_user.id, Contact.accepted==False).value(Contact.requestee_id))
	#generate the available ask for friends list
	requestable_users = list()
	for user in users:
		if user.id not in (already_requestee_id or accepted_requestees or accepted_requesters) and user != current_user:
			requestable_users.append(user)						
	return render_template('base/user.html', username=username, title = username, users=requestable_users, already_requester_id=already_requester_id)

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
	db.session.commit()
	return redirect(url_for('.user', username = current_user.username))

