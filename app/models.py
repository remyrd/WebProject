from app import db, login_manager
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin



class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), nullable = True, unique = True, index = True)
	username = db.Column(db.String(64), nullable = False, unique = True, index = True)
	is_admin = db.Column(db.Boolean, default=False)
	password_hash = db.Column(db.String(128))
	avatar_hash = db.Column(db.String(32))
	#contacts_requests = db.relationship('Contact', backref = 'asker', lazy='dynamic')
	
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
		
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))
	
class Rooms(db.Model):
	__tablename__='rooms'
	id = db.Column(db.Integer, primary_key = True)
	roomname = db.Column(db.String(64), nullable = False, unique = True, index = True)
	password_hash = db.Column(db.String(128))
	admin = db.Column(db.Integer, nullable = False)
	
	def __repr__(self):
		return '<Room %r>' % (self.roomname)
	