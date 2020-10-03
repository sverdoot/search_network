'''

  flask_ponywhoosh.form module
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Perform full-text searches over your database with Pony ORM and PonyWhoosh,
  for flask applications.

  :copyright: (c) 2015-2018 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask_wtf          import FlaskForm
from wtforms            import StringField, SubmitField
from wtforms            import BooleanField, SelectField
from wtforms.validators import Required

#from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from flask_login import current_user
from search_network import Person, Project, Idea, Department, Area


# class SearchForm(FlaskForm):
#   """This is the searching form that we will be use to make our search
#   engine website.

#   Attributes:
#       except_field (StringField): Fields you do not want to include in the search results.
#       fields (StringField): Fields, separated by comma,  where you want to search.
#       models (StringField): Models, separated by comma, where you want to search.
#       query (StringField): What you want to search.
#       something (BooleanField): Option to literal search first, but in case there are no results available, it performs a search with wild_cards.
#       submit (SubmitField): Button to submit the form.
#       wildcards (BooleanField): Checkbox
#   """

#   add_wildcards = BooleanField('Add Wildcards', default=True)
#   except_field  = StringField('Except in Fields')
#   fields        = StringField('Fields')
#   models        = StringField('Models')
  
#   query         = StringField('What are you looking for?')
  
#   something     = BooleanField('Something')
#   submit        = SubmitField('Submit')


# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')


# class LoginForm(FlaskForm):
#     username = StringField('username',
#                         validators=[DataRequired()])  
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')


# class UpdateForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

#     submit = SubmitField('Update user info')
#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('That username is taken. Please choose a different one.')

#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('That email is taken. Please choose a different one.')  


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()]) 
    image = FileField('Attach a picture..', validators=[FileAllowed(['jpg', 'png'])]) 
    content = TextAreaField('Content' , validators=[DataRequired()])
    submit = SubmitField('Post')    


class NewStoryForm(FlaskForm):
    image = FileField('Attach a picture..', validators=[FileAllowed(['jpg', 'png'])]) 
    submit = SubmitField('Post') 


class ChattingForm(FlaskForm):
    message = TextAreaField('Type...', validators=[DataRequired()]) 
    submit = SubmitField('Send') 


class SearchForm(FlaskForm):
    searched = StringField('Search' , validators=[DataRequired()])
    submit = SubmitField('Search')


# class RequestResetForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError('There is no account with that email. You must register first.')


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')


# class NewProjectForm(FlaskForm):


# class NewIdeaForm(FlaskForm):


# class DepartmentsForm(FlaskForm):


# class ProjectsForm(FlaskForm):


# class IdeasForm(FlaskForm):


# class SlackChannelsForm(FlaskForm):

                