from flask import Flask
from flask_mail import Mail, Message
import os


server = Flask(__name__,instance_relative_config=False)

server.config['SECRET_KEY'] = os.environ['SECRET_KEY']
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
server.config['SECURITY_PASSWORD_SALT'] = os.environ['SECRET_SALT']
server.config['SECURITY_RECOVERABLE'] = True
server.config.update(
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 587,
	MAIL_USE_TLS=True,
	MAIL_USERNAME=os.environ['EMAIL_USER'],
	MAIL_PASSWORD=os.environ['EMAIL_PASS']
	)

mail = Mail(server)
