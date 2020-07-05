from flask_wtf import FlaskForm
from models import User
from wtforms import PasswordField, StringField, ValidationError, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, Length


###############################
###### Register new user ######
###############################

class RegisterUser(FlaskForm):

    email = StringField('Email: ', validators = [InputRequired(), Email(message = 'Enter a valid email address.')])
    password = PasswordField('Password: ', validators = [InputRequired(), Length(min = 4, message = 'Password length must be greater than 4.')])
    username = StringField('User Name: ', validators = [InputRequired()])
    submit = SubmitField('Register')

    def check_mail(self, data):
        if User.query.filter_by(email = data).first():
            raise ValidationError('Your email is already registered.')

    def check_username(self, data):
        if User.query.filter_by(username = data).first():
            raise ValidationError('This username is already registered.')


###############################
###### Login form #############
###############################

class LoginUser(FlaskForm):

    email = StringField('Email: ', validators = [InputRequired(), Email(message = 'Enter a valid email address.')])
    password = PasswordField('Password: ', validators = [InputRequired()])
    check = BooleanField('Remember me ')
    submit = SubmitField('Log In')
