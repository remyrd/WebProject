from app import db




class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), nullable = True, unique = True, index = True)
	username = db.Column(db.String(64), nullable = False, unique = True, index = True)
	is_admin = db.Column(db.Boolean, default=False)
	password_hash = db.Column(db.String(128))
	avatar_hash = db.Column(db.String(32))
	contacts_requests = db.relationship('Contact', backref = 'asker', lazy='dynamic')
	def __repr__(self):
		return '<User %r>' % (self.username)

class Contact(db.Model):
	__tablename__='contacts'
	id = db.Column(db.Integer, primary_key = True)
	request_from = db.Column(db.Integer, db.ForeignKey('user.id'))
	request_to = db.Column(db.Integer)
	confirmed = db.Column(db.Boolean, default = False)
	
	def __repr__(self):
		return '<Contact ID %r>' % (self.id)
	
class Rooms(db.Model):
	__tablename__='rooms'
	id = db.Column(db.Integer, primary_key = True)
	roomname = db.Column(db.String(64), nullable = False, unique = True, index = True)
	password_hash = db.Column(db.String(128))
	admin = db.Column(db.Integer, nullable = False)
	
	def __repr__(self):
		return '<Room %r>' % (self.roomname)
	