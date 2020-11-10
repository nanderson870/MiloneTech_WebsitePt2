from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    email = StringField('Username',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Thighs', validators=[DataRequired()])
    remember = BooleanField('Ass')
    submit = SubmitField('Submit')

class SettingsForm(FlaskForm):
    email = StringField('Rocking',
                        validators=[DataRequired(), Email()])
    password = PasswordField('On', validators=[DataRequired()])
    remember = BooleanField('Crazy')
    submit = SubmitField('Add Trigger')

