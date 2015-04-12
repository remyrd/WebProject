from . import contacts
from flask import render_template, redirect, url_for, flash, request
from ..models import User, Contact
from flask_login import current_user, login_required
from app import db
from ..base.routes import map_current_user_contacts
from flask.templating import render_template_string

@login_required
@contacts.route('/add/<id>', methods=['POST','GET'])
def add(id):
    new_contact = Contact(requester_id=current_user.id, requestee_id=id)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('base.user', username = current_user.username))

@contacts.route('/confirm/<id>', methods=['GET','POST'])
@login_required
def confirm(id):
    confirmation = Contact.query.filter_by(requester_id=id,requestee_id=current_user.id).first()
    if confirmation:
        confirmation.accepted=True
    db.session.merge(confirmation)
    db.session.commit()
    return redirect(url_for('.requests'))


@login_required
@contacts.route('/delete_request/<id>', methods=['POST','GET'])
def delete_request(id):
    unwanted_person=Contact.query.filter_by(requester_id=id, requestee_id=current_user.id).first()
    db.session.delete(unwanted_person)
    db.session.commit()
    return redirect(url_for('.requests'))

@contacts.route('/requests')
@login_required
def requests():
    map_current_user_contacts()    
    users = User.query.all()
    return render_template("contacts/requests.html", users=users, requests = len(current_user.already_requestee_id), already_requestee_id = current_user.already_requestee_id)


@login_required
@contacts.route('/delete_contact/<id>', methods=['POST','GET'])
def delete_contact(id):
    unwanted_person=Contact.query.filter_by(requester_id=id, requestee_id=current_user.id).first()
    if unwanted_person==None:
        unwanted_person=Contact.query.filter_by(requester_id=current_user.id, requestee_id=id).first()
        
    db.session.delete(unwanted_person)
    db.session.commit()
    return redirect(url_for('.list_friends'))
        
@login_required
@contacts.route('/list_friends')
def list():
    map_current_user_contacts()    
    return render_template("contacts/list_friends.html", friends = current_user.friends)

@login_required
@contacts.route('/search', methods=['POST','GET'])
def search():
    name=request.form['query']
    listed_users=[]
    map_current_user_contacts()
    for user in User.query.all():
        if name in user.username:
            listed_users.append(user)
    return render_template('contacts/search_results.html',name = name, listed_users=listed_users)
    

@login_required
@contacts.route('/show_profile/<id>')
def show_profile(id):
    friend=User.query.filter_by(id=id).first()
    return render_template("contacts/friend_profile.html",friend=friend)

    
