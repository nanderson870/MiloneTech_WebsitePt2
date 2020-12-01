from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    name = StringField('Full Name',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    newEmail = StringField('Update Email Info')
    password = PasswordField('New Password')
    confirmPassword = PasswordField('Confirm New Password')
    phoneNumber = StringField('New Phone Number')
    submitAccountInfo = SubmitField('Submit Account Info')

class SensorAccountForm(FlaskForm):
    sensorID = StringField('Sensor ID')
    submitSensor = SubmitField('Submit Sensor')


class SettingsForm(FlaskForm):
    sensorID = SelectField('Select to add trigger to Sensor', choices = [('', 'Choose your Sensor')])
    textOrEmail = SelectField('Text or Email', choices = [(1, 'text'), (0, 'email')])
    level = StringField('Level')
    allSensorNames = SelectField('TODO: change in routes', choices = [('yes', 'no'), ('no', 'yes')])
    newSensorName = StringField('Enter Sensor\'s Name')
    sensorGroup = SelectField('ll', choices = [('lol', 'lol'), ('nope', 'nope')])
    newSensorGroup = StringField('Enter New Sensor Group')
    submit = SubmitField('Add Trigger')
    allTriggerValues = SelectField('who cares', choices = [])
