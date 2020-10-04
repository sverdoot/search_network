import ast
from flask import Flask
from flask_migrate import Migrate , MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_session import Session


from datetime import datetime, timedelta, date

from pony.orm import *
from pony.flask import Pony


from search_network.models import db

app = Flask(__name__)
Pony(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../site.db'
app.config['SESSION_TYPE'] = 'filesystem'
bcrypt = Bcrypt(app)

Session(app)
socketio = SocketIO(app, manage_session=False)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lamma2019c@gmail.com'
app.config['MAIL_PASSWORD'] = 'jablouniss'
#mail = Mail(app)
#mobility = Mobility(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand )


from search_network import routes