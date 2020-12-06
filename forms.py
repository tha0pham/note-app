from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 10)])

    lastname = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', [Email(message='Not a valid email address.'), DataRequired()])

    password = PasswordField('Password', [DataRequired(message="Please enter a password."), EqualTo('confirmPassword', message='Passwords must match')])

    confirmPassword = PasswordField('Confirm Password', validators=[Length(min=6, max=10)])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Log In')

