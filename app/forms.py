# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('analyst', 'Analyst'), ('viewer', 'Viewer')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class DatasetUploadForm(FlaskForm):
    file = FileField('Dataset File', validators=[DataRequired()])
    submit = SubmitField('Upload & Preview')

class CleanTransformForm(FlaskForm):
    missing_strategy = SelectField('Missing Strategy', choices=[
        ('', '-- Select Strategy --'),
        ('drop', 'Drop Rows with Missing Values'),
        ('fill_mean', 'Fill with Mean'),
        ('fill_median', 'Fill with Median'),
        ('fill_zero', 'Fill with 0'),
    ])
    submit = SubmitField('Apply Transformations')
