from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

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