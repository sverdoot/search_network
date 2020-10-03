# from search_network import app , manager, db

# @db_session
# def populate_database():
#     import pandas as pd
#     columns = ['id', 'Name', 'mail', 'dunno', 'dept', 'role', 'skills']
#     df = pd.read_csv('Employees.csv', names=columns, index_col=0)
#     employees = []
#     departments = []
#     all_skills = []

#     for _, row in df.iterrows():
#         print(row['skills'])
#         name = row['Name'].split(' ')
#         mail = row['mail']
#         dept = row['dept']
#         skills = ast.literal_eval(row['skills'])

#         if Department.get(name=dept) is None:
#             departments.append(Department(name=dept))
#         for skill in skills:
#             if select(s for s in Skill).count() == 0 or Skill.get(name=skill) is None:
#                 print(skill)
#                 all_skills.append(Skill(name=skill))
#         department = select(d for d in Department if d.name == dept)[:][0]
#         employees.append(Person(name=name[0], surname=name[1], mail=mail, department=department, skills=select(s for s in Skill if s.name in skills)[:]))
#         department.persons.add(employees[-1])

#     commit()

# if __name__ == '__main__':
# 	manager.run()s