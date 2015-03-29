from . import auth
from flask import render_template, redirect, url_for, flash
from .forms import LoginForm
from ..models import User
from flask_login import login_user



@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("username or password incorrect")
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        return redirect(url_for('base.user', username = user.username))
    return render_template ('auth/login.html', form = form)
