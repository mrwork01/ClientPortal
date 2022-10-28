from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from  scripts.database import db, User, Role, Orders, Customers
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField

def queryCompany():
	return Customers.query

class RegistrationForm(FlaskForm):
	email = EmailField('Email', [
							validators.DataRequired(),
							validators.Email(message="Please Enter a Valid Email Address")])
	company = QuerySelectField("Company", query_factory=queryCompany, get_label='name')
	first = StringField('First Name', [validators.Length(min=2, max=20)])
	last = StringField('Last Name', [validators.Length(min=2, max=20)])
	password = PasswordField('Password', [
							 validators.DataRequired(),
							 validators.EqualTo('confirm', message="Password Must Match")])
	confirm = PasswordField('Confirm Password')
	submit = SubmitField("Submit")

