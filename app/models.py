from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin



class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), nullable = True, unique = True, index = True)
	username = db.Column(db.String(64), nullable = False, unique = True, index = True)
	is_admin = db.Column(db.Boolean, default=False)
	password_hash = db.Column(db.String(128), nullable = False)
	avatar_hash = db.Column(db.String(32))
	contacts_requests = db.relationship('Contact', backref = "requester", lazy = "dynamic" )
	room_administrated = db.relationship('Room', backref = 'room_admin')
	
	def __repr__(self):
		return '<User %r>' % (self.username)
	
	@property
	def password(self):
		raise AttributeError("password is not readable")
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)	
	
	accepted_requesters = [] 
	accepted_requestees = [] 
	already_requestee_id = []
	already_requester_id = []
	requestable_users = []
	
			
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))
	
class Room(db.Model):
	__tablename__='rooms'
	id = db.Column(db.Integer, primary_key = True)
	roomname = db.Column(db.String(64), nullable = False, unique = True, index = True)
	password_hash = db.Column(db.String(128))
	admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	def __repr__(self):
		return '<Room %r>' % (self.roomname)

class Contact(db.Model):
	__tablename__ = "contacts"
	id = db.Column(db.Integer, primary_key = True)
	requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	requestee_id = db.Column(db.Integer, nullable = False)
	accepted = db.Column(db.Boolean, default=False)
	
	