from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL

# AUTH LOGIN FORM
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

# AUTH REGISTRATION FORM
class UserRegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password')
    submit_button = SubmitField('Submit')

# LINK SUBMISSION FORM
class LinkSubmissionForm(FlaskForm):
    listed_link = StringField('Link', validators=[DataRequired(), URL(message='Please enter a valid URL.')])
    link_title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    is_public = BooleanField('Is Public?')
    submit_button = SubmitField('Submit')