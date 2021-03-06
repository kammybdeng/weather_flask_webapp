from weatherflaskwebapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	cities = db.relationship('City', backref='user', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"


class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

	def __repr__(self):
		return f"City('{self.name}', '{self.user_id}')"