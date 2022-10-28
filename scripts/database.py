from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import os, sys
sys.path.append("/Users/marcwork/OneDrive - (na)/documents/Software/client_portal")

from server import server
from run import user_datastore


db = SQLAlchemy(server)

#Create Role to User Relationship
roles_users = db.Table('roles_users',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

	
class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(225))
	name = db.Column(db.String(225), unique=True)
	active = db.Column(db.Boolean)
	roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
	orders_rel = db.relationship('Orders')
	customer_name = db.Column(db.String(255), db.ForeignKey('customers.name'))


class Role(db.Model,RoleMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40))
	description = db.Column(db.String(255))

class Customers(db.Model):
	name = db.Column(db.String(225), primary_key=True)
	company_rel = db.relationship('User')

class Orders(db.Model):
	wo_num = db.Column(db.Integer, primary_key=True)
	address = db.Column(db.String(225))
	status = db.Column(db.String(225))
	next_date = db.Column(db.String(225))
	manager_id = db.Column(db.String(225), db.ForeignKey('user.name'))

#-------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	db.create_all()

	'''db.session.add(Role (name='admin',description="Administrator"))
	db.session.add(Role (name='client',description="Client"))
	db.session.add(Customers (name='Customer #1'))
	db.session.add(Customers (name='Customer #2'))
	db.session.add(Customers (name='Customer #3'))
	db.session.commit()'''

	user_datastore.create_user(
			email = 'admin@clientportal.com',
			name= 'Smith, John',
			password = hash_password('password'),
			customer_name = 'Customer #1',
			roles = ['admin']
		)
		db.session.commit()
