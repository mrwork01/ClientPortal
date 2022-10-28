from flask_sqlalchemy import SQLAlchemy
from  scripts.database import db, User, Role, Orders, Customers

class databaseCall:
	def __init__(self, table=None, role='client', manager=None):
		self.table = table if role is not None else table
		self.role = role if role is not 'client' else role
		self.manager = manager if manager is not 'client' else manager


	def oneColumn(self, col_name):
		data_table = self.table.query.all()

		data = []

		for i in range(len(data_table)):
			data.append(getattr(data_table[i], col_name))

		print(data)

		return data

	def orderFilter(self, wo_num='', filter_manager='', status='Open'):

		wo_num = wo_num if wo_num != '' else wo_num
		filter_manager = filter_manager if filter_manager != '' else filter_manager
		status = status if status != 'open' else status

		raw_data = db.session.query(Orders).join(User,Customers).add_columns(Customers.name)
		
		#------------------------------------------------------------------------------------
		#Customer
		if self.role != 'admin':
			company = db.session.query(User).filter(User.name==self.manager).first().customer_name
			raw_data = raw_data.filter(Customers.name==company)
		#------------------------------------------------------------------------------------
		#Status	
		if status != 'Open':
			raw_data = raw_data.filter(Orders.status==status)

		elif status == 'Open':
			raw_data = raw_data.filter(Orders.status!='Complete')
		#------------------------------------------------------------------------------------
		#WO_num
		if wo_num != '':
			raw_data = raw_data.filter(Orders.wo_num==wo_num)
		#------------------------------------------------------------------------------------
		#Manager
		if filter_manager != '':
			raw_data = raw_data.filter(Orders.manager_id==filter_manager)

		raw_data = raw_data.all()

		data = []
		
		for i in range(len(raw_data)):
			data_dict = raw_data[i][0].__dict__
			data_dict['company'] = raw_data[i][1]
			data_dict.pop('_sa_instance_state', None)
			data.append(data_dict)

		return data

	def getUserList():
		raw_data = db.session.query(User).all()

		data = []

		for i in range(len(raw_data)):
			data_dict = raw_data[i].__dict__
			data_dict.pop('_sa_instance_state', None)
			data.append(data_dict)

		return data

	def getAssociates(self,):
		users_company = db.session.query(User).filter(User.name == self.manager).first().customer_name
		if self.role == 'admin':
			raw_data = db.session.query(User).all()
		else:
			raw_data = db.session.query(User).filter(User.customer_name == users_company).all()

		data = []

		for i in range(len(raw_data)):
			data_dict = raw_data[i].name
			data.append(data_dict)


		return data


							

