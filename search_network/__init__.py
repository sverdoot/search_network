# '''

#   flask_ponywhoosh module
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#   Perform full-text searches over your database with Pony ORM and PonyWhoosh,
#   for flask applications.

#   :copyright: (c) 2015-2018 by Jonathan Prieto-Cubides & Felipe Rodriguez.
#   :license: MIT (see LICENSE.md)

# '''

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

# import jinja2
# import os

# from ponywhoosh  import PonyWhoosh as MyPonyWhoosh
# from ponywhoosh  import search, full_search, delete_field
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

#     if self.debug:
#       print('PONYWHOOSH_DEBUG: ', self.debug)
#       print('PONYWHOOSH_INDEXES_PATH : ', self.indexes_path)
#       print('PONYWHOOSH_MIN_STRING_LEN : ', self.search_string_min_len)
#       print('PONYWHOOSH_TEMPLATE_PATH: ', self.template_path)
#       print('PONYWHOOSH_URL_ROUTE: ',  self.url_route)
#       print('PONYWHOOSH_WRITER_TIMEOUT: ', self.writer_timeout)

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
#from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate , MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_session import Session
from flask_mail import Mail
from flask_mobility import Mobility

from datetime               import datetime, timedelta, date

from pony.orm import *



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../site.db'
app.config['SESSION_TYPE'] = 'filesystem'
bcrypt = Bcrypt(app)
db = Database() #SQLAlchemy(app)

#@pw.register_model('id', 'name', 'department', 'skills', 'areas')
class Project(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    department = Required('Department')
    persons = Set('Person', reverse='projects', nullable=True)
    skills = Set('Skill', nullable=True)
    areas = Set('Area', nullable=True)
    requested_by = Set('Person', nullable=True)


#@pw.register_model('id', 'name', 'surname', 'skills', 'projects')
class Person(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    surname = Required(str)
    mail = Optional(str, nullable=True)
    department = Required('Department')
    skills = Set('Skill', nullable=True)
    projects = Set(Project, nullable=True)
    ideas = Set('Idea', nullable=True)
    in_waiting_list = Set('Project', reverse='requested_by', nullable=True)
    areas = Set('Area')


#@pw.register_model('id', 'name', '')
class Idea(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    likes = Optional(int, nullable=True)
    dislikes = Optional(int, nullable=True)
    inventor = Required(Person)
    areas = Set('Area', nullable=True)


#@pw.register_model('id')
class Department(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    projects = Set(Project, nullable=True)
    persons = Set(Person, nullable=True)


#@pw.register_model('id', 'name')
class Skill(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    persons = Set(Person, nullable=True)
    projects = Set(Project, nullable=True)


#@pw.register_model('id', 'name')
class Area(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    projects = Set(Project, nullable=True)
    ideas = Set(Idea, nullable=True)
    persons = Set(Person)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(str)
    time = Required(datetime)
    sent_by = Required(int)
    sent_to = Required(int)

db.bind('sqlite', 'example.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def populate_database():
    import pandas as pd
    columns = ['id', 'Name', 'mail', 'dunno', 'dept', 'role', 'skills']
    df = pd.read_csv('Employees.csv', names=columns, index_col=0)
    employees = []
    departments = []
    all_skills = []

    for _, row in df.iterrows():
        print(row['skills'])
        name = row['Name'].split(' ')
        mail = row['mail']
        dept = row['dept']
        skills = ast.literal_eval(row['skills'])

        if Department.get(name=dept) is None:
            departments.append(Department(name=dept))
        for skill in skills:
            if select(s for s in Skill).count() == 0 or Skill.get(name=skill) is None:
                print(skill)
                all_skills.append(Skill(name=skill))
        department = select(d for d in Department if d.name == dept)[:][0]
        employees.append(Person(name=name[0], surname=name[1], mail=mail, department=department, areas=[], skills=select(s for s in Skill if s.name in skills)[:]))
        department.persons.add(employees[-1])

    commit()


populate_database()
#loginManager = LoginManager(app)
#loginManager.login_view = 'login'
#loginManager.login_message_category = 'info'

Session(app)
socketio = SocketIO(app , manage_session=False)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lamma2019c@gmail.com'
app.config['MAIL_PASSWORD'] = 'jablouniss'
mail = Mail(app)
mobility = Mobility(app)
migrate = Migrate(app , db)
manager = Manager(app)
manager.add_command('db' , MigrateCommand )


from search_network import routes