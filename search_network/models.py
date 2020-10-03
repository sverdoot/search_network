import os

from datetime               import datetime, timedelta, date
#from flask                  import Flask, jsonify, render_template
from flask_bootstrap        import Bootstrap
#from flask_ponywhoosh       import PonyWhoosh
from flask_script           import Manager, Shell
from pony.orm               import *
#from pony.orm.serialization import to_json
from datetime import datetime
from pony.orm import *


#db = Database()
from search_network import db


class Project(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    department = Required('Department')
    persons = Set('Person')
    skills = Set('Skill')
    areas = Set('Area')
    content = Optional(str)


class Person(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    surname = Optional(str)
    department = Required('Department')
    skills = Set('Skill')
    projects = Set(Project)
    ideas = Set('Idea')
    areas = Set('Area')


class Idea(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    likes = Optional(int)
    dislikes = Optional(int)
    inventor = Required(Person)
    areas = Set('Area')
    content = Optional(str)


class Department(db.Entity):
    id = PrimaryKey(int, auto=True)
    projects = Set(Project)
    persons = Set(Person)


class Skill(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    persons = Set(Person)
    projects = Set(Project)


class Area(db.Entity):
    id = PrimaryKey(int, auto=True)
    project = Optional(Project)
    name = Required(str)
    ideas = Set(Idea)
    person = Set(Person)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Optional(str)
    time = Required(datetime)
    sent_by = Required(int)
    sent_to = Required(int)


db.generate_mapping(create_tables=True)