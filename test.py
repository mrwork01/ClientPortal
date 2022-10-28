from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from scripts.database import db, User, Role, Orders, Customers
from server import server
from scripts.flask_db_calls import databaseCall


data = databaseCall(role='admin', manager='Work, Marc').getAssociates()

print(data)
#print(data)

#test = db.session.query(Orders).join(User,Customers).add_columns(Customers.name).all()
#test_dict = test[0][0].__dict__
#test_dict.pop('_sa_instance_state', None)
#test_dict['Customer'] = test[0][1]
#print(test_dict)

#for i in test:
	#print (i.__dict__)

