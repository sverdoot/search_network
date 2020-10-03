# import jinja2
# import os

# from .views      import IndexView


# __all__     = ['PonyWhoosh', 'search', 'full_search', 'delete_field']
# __author__  = "Jonathan Prieto-Cubides & Felipe Rodriguez"
# basedir     = os.path.abspath(os.path.dirname(__file__))

# class PonyWhoosh(MyPonyWhoosh):

#   debug           = False
#   indexes_path    = 'ponywhoosh_indexes'
#   writer_timeout  = 2
#   url_route       = '/search/'
#   template_path   = os.path.join(basedir, 'templates')
#   search_string_min_len = 2


#   def __init__(self, app=None):
#     super(PonyWhoosh, self).__init__()

#     if app is not None:
#       self.init_app(app)

#     if not os.path.exists(self.indexes_path):
#       os.makedirs(self.indexes_path)

#   def init_app(self, app):
#     """Initializes the App.

#     Args:
#         app (TYPE): Description

#     Returns:
#         TYPE: Description
#     """

#     config = app.config.copy()
#     self.debug        = config.get('PONYWHOOSH_DEBUG', self.debug)
#     self.indexes_path = config.get('PONYWHOOSH_INDEXES_PATH',  self.indexes_path)
#     self.search_string_min_len = config.get('PONYWHOOSH_MIN_STRING_LEN', self.search_string_min_len)
#     self.template_path  = config.get('PONYWHOOSH_TEMPLATE_PATH', self.template_path)
#     self.url_route      = config.get('PONYWHOOSH_URL_ROUTE', self.url_route)
#     self.writer_timeout = config.get('PONYWHOOSH_WRITER_TIMEOUT', self.writer_timeout)


#     loader = jinja2.ChoiceLoader([
#         app.jinja_loader
#       , jinja2.FileSystemLoader(self.template_path)
#     ])

#     app.jinja_loader = loader
#     app.add_url_rule(
#         self.url_route
#       , view_func=IndexView.as_view(self.url_route
#         , pw=self
#         , action_url_form=self.url_route
#         )
#     )

import ast
from flask import Flask
from flask_migrate import Migrate , MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_session import Session
from flask_mail import Mail
from flask_mobility import Mobility

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

#loginManager = LoginManager(app)
#loginManager.login_view = 'login'
#loginManager.login_message_category = 'info'

Session(app)
socketio = SocketIO(app, manage_session=False)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lamma2019c@gmail.com'
app.config['MAIL_PASSWORD'] = 'jablouniss'
mail = Mail(app)
mobility = Mobility(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand )


from search_network import routes