#Test
from flask import Flask, request, render_template, redirect, url_for,jsonify, flash
from flask_security import Security, SQLAlchemyUserDatastore, \
    	login_required, roles_required, current_user
from flask_security.utils import hash_password
import json
from scripts.database import db, User, Role, Orders, Customers
from scripts.flask_db_calls import databaseCall
from scripts.formValidation import RegistrationForm
from server import server, mail
import os

port = int(os.environ.get("PORT", 8000))

#-----------------------------------------------------------------

#Connect Database to Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(server, user_datastore)

#-------------------------------------------------------------------------------
# get_user_first(): 
# Returns the user's first name for display on each page
#-------------------------------------------------------------------------------

def get_user_first():
	curr_user = current_user.name
	name_string = curr_user.split(',')
	curr_user = name_string[1]
	return curr_user

#-------------------------------------------------------------------------------
# get_user_first(): 
# Returns the user's first name for display on each page
#-------------------------------------------------------------------------------

def get_role():
	if current_user.has_role('admin'):
		role = 'admin'
	else:
		role = 'client'

	return role

#-------------------------------------------------------------------------------
# index(): 
# Directs user to correct side of applicaiton based on permissions (ie. admin or client)
#-------------------------------------------------------------------------------


@server.route('/')
@login_required
def index():
	if current_user.has_role('admin'):
		return redirect('/admin')

	if current_user.has_role('client'):
		return redirect('/clientOrders')
		
#-------------------------------------------------------------------
# ClientOrders()
# Renders Client user view
#-------------------------------------------------------------------

@server.route("/clientOrders", methods=['POST', 'GET'])
@login_required
def clientOrders():
	role = get_role()
	user_first = get_user_first()

	db_inst = databaseCall(role=role, manager=current_user.name)
	associates = db_inst.getAssociates()
	client_jobs = db_inst.orderFilter()

	return render_template('clientOrders.html', client_jobs=client_jobs, user_first=user_first, associates=associates)

#-------------------------------------------------------------------
# admin()
# Renders admin view
#-------------------------------------------------------------------


@server.route('/admin', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def admin():
	role = get_role()
	user_first = get_user_first()

	db_inst = databaseCall(role=role, manager=current_user.name)
	associates = db_inst.getAssociates()
	client_jobs = db_inst.orderFilter()
		
	return render_template('jobList.html', client_jobs=client_jobs, user_first=user_first, associates=associates)

#-------------------------------------------------------------------
# orderFilter()
# Receives input from filter POST on Client & Admin view, then
# returns the appropriate table to the Ajax call
#-------------------------------------------------------------------

@server.route('/orderFilter', methods=['POST'])
def orderFilter():

	role = get_role()

	wo_filter = request.json.get('wo_num')
	status_filter = request.json.get('status')
	manager_filter = request.json.get('manager')

	db_inst = databaseCall(role=role, manager=current_user.name,)
	client_jobs = db_inst.orderFilter(wo_num=wo_filter, status=status_filter, filter_manager=manager_filter)

	if current_user.has_role('admin'):
		return render_template('filteredTable.html', client_jobs=client_jobs)

	if current_user.has_role('client'):
		return render_template('clientTable.html', client_jobs=client_jobs)

#-------------------------------------------------------------------
# updateStatus()
# Receives input from the Status change POST and updates the Orders
# database
#-------------------------------------------------------------------

@server.route('/updateStatus', methods=['POST'])
def updateStatus():

	#Assign from POST
	wo_num = request.json.get('wo_num')
	status = request.json.get('status')

	#Update Database
	db.session.query(Orders).filter(Orders.wo_num==wo_num).update({'status': status})
	db.session.commit()

	return wo_num

#-------------------------------------------------------------------
# updateDate()
# Receives input from the Next Date change POST and updates the Orders
# database
#-------------------------------------------------------------------

@server.route('/updateDate', methods=['POST'])
def  updateDate():

	wo_num = request.json.get('wo_num')
	date = request.json.get('date')

	db.session.query(Orders).filter(Orders.wo_num==wo_num).update({'next_date': date})
	db.session.commit()

	return "Update Successful"

#-------------------------------------------------------------------
# users()
# Renders the list of users page
#-------------------------------------------------------------------

@server.route('/users')
@roles_required('admin')
def users():
	user_list = databaseCall.getUserList()
	curr_user = get_user_first()

	return render_template('users.html', user_list=user_list, curr_user=curr_user)

#-------------------------------------------------------------------
# registered()
# Renders a page letting the user know the registration was complete
#-------------------------------------------------------------------

@server.route('/registered')
def registered():
	return render_template('registered.html')

#-------------------------------------------------------------------
# register()
# Renders the registration page and receives the registration form
# POST and adds user to Users database
#-------------------------------------------------------------------

@server.route('/register', methods=['POST', 'GET'])

def register():
	#------------------------------------------------------------------
	raw_data = databaseCall(table=Customers).oneColumn(col_name='name')
	cust_list = []

	for i in range(len(raw_data)):
		cust_dict = {'name': raw_data[i], 'value': raw_data[i]}
		cust_list.append(cust_dict)

	#------------------------------------------------------------------
	form = RegistrationForm(request.form)

	if request.method == 'POST' and form.validate_on_submit():
		#cust_id = db.session.query(Customers).filter(Customers.name == (request.form.get('company'))).first()
		user_datastore.create_user(
			email = form.email.data,
			name= '{}, {}'.format(form.last.data,form.first.data),
			password = hash_password(form.password.data),
			customer_name = form.company.data.name,
			roles = ['client']
		)
		db.session.commit()

		flash('Use Registered')
		return redirect('/')

	if request.method == 'POST' and form.validate_on_submit() == False:
		print(form.password.errors)

	return render_template('register.html', form=form)

#-------------------------------------------------------------------
# addJobs()
# Renders the Add Orders page, receives the add order form POST and 
# adds it to the Orders database
#-------------------------------------------------------------------

@server.route('/addJob', methods=['POST', 'GET'])
@roles_required('admin')
def addJob():
	cust_list = databaseCall(table=Customers).oneColumn(col_name='name')
	
	curr_user = get_user_first()

	if request.method =='POST':
		user_id = db.session.query(User).filter(User.name == (request.form.get('owner'))).first()
		order = Orders(wo_num=request.form.get('wo_num'),
				   	   address=request.form.get('address'),
				   	   status=request.form.get('status'),
				   	   manager_id=request.form.get('owner'))

		db.session.add(order)
		db.session.commit()



	return render_template('addJob.html', curr_user=curr_user, cust_list=cust_list)

#-------------------------------------------------------------------
# dynDrop()
# Receives the company dropdown POST from add orders form and returns
# a list of managers for that company to populate managers dropdown 
#-------------------------------------------------------------------

@server.route('/dynDrop', methods=['POST'])
def dynDrop():

	company = request.json.get('company')

	raw_data = db.session.query(User).filter(User.customer_name == company).all()

	data = {}

	for i in range(len(raw_data)):
		data_dict = raw_data[i].name
		data['company{}'.format(i)] = data_dict

	data_out = json.dumps(data)

	return data
#-------------------------------------------------------------------
# main()
#-------------------------------------------------------------------
if __name__ == '__main__':
	server.run(host='0.0.0.0', port=port)

