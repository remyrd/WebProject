from flask import render_template, redirect, flash
from . import chat
from .forms import LoginForm
from config import OPENID_PROVIDERS
#toy example

providers = OPENID_PROVIDERS
@chat.route('/')
def index():
	return render_template('chat/index.html')

@chat.route('/user/<username>')
def user(username):
	return render_template('chat/user.html', username=username, title = username)

@chat.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
		return redirect('/')
	
	return render_template('login.html',form = form, title = 'Sign In',providers=providers)


