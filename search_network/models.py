import os

from datetime               import datetime, timedelta, date
from flask_bootstrap        import Bootstrap
from flask_script           import Manager, Shell
from pony.orm               import *
from datetime import datetime
from pony.orm import *
import ast


db = Database() 


class Project(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    department = Required('Department')
    persons = Set('Person', reverse='projects', nullable=True)
    skills = Set('Skill', nullable=True)
    areas = Set('Area', nullable=True)
    requested_by = Set('Person', nullable=True)

    # def get_skills(self):
    #     return 


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


class Idea(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    likes = Optional(int, nullable=True)
    dislikes = Optional(int, nullable=True)
    inventor = Required(Person)
    areas = Set('Area', nullable=True)
    skills = Set('Skill', nullable=True)
    department = Optional('Department')


class Department(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    projects = Set(Project, nullable=True)
    persons = Set(Person, nullable=True)
    ideas = Set(Idea)


class Skill(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    persons = Set(Person, nullable=True)
    projects = Set(Project, nullable=True)
    ideas = Set(Idea, nullable=True)


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
    if select(p for p in Person).count() > 0: return
    import pandas as pd
    columns = ['id', 'Name', 'mail', 'dunno', 'dept', 'role', 'skills']
    df = pd.read_csv('Employees.csv', names=columns, index_col=0)
    employees = []
    departments = []
    all_skills = []

    for _, row in df.iterrows():
        name = row['Name'].split(' ')
        mail = row['mail']
        dept = row['dept']
        skills = ast.literal_eval(row['skills'])

        if Department.get(name=dept) is None:
            departments.append(Department(name=dept))
        for skill in skills:
            if select(s for s in Skill).count() == 0 or Skill.get(name=skill) is None:
                all_skills.append(Skill(name=skill))
        department = select(d for d in Department if d.name == dept)[:][0]
        employees.append(Person(name=name[0], surname=name[1], mail=mail, department=department, areas=[], skills=select(s for s in Skill if s.name in skills)[:]))
        department.persons.add(employees[-1])

    commit()


populate_database()