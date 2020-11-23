from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import flask_website.dbAPI.app as db


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
    email = StringField('Username',
                        validators=[DataRequired(), Email()])
    password = PasswordField('SensorID', validators=[DataRequired()])
    remember = BooleanField('Ass')
    submit = SubmitField('Submit')

class SettingsForm(FlaskForm):
    email = StringField('Rocking',
                        validators=[DataRequired(), Email()])
    password = PasswordField('On', validators=[DataRequired()])
    remember = BooleanField('Crazy')
    submit = SubmitField('Add Trigger')

class RequestResetForm(FlaskForm):
    email = StringField('Username',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):

        user_email = db.accounts.get_id_by_email(email.data)
        print(user_email)
        if not user_email:
            raise ValidationError('That Email doesnt Exist. You must Regsiter First')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
