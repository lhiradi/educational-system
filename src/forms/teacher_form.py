from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, EmailField, DateField, 
)
from wtforms.validators import DataRequired, Length, Email, Optional


class TeacherForm(FlaskForm):
    teacher_id = StringField('Teacher ID', validators=[DataRequired(), Length(min=4, max=13)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    national_id = StringField('National ID', validators=[Optional(), Length(max=10)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Register')
    
class TeacherProfileForm(FlaskForm):
    teacher_id = StringField('Teacher ID', validators=[DataRequired(), Length(min=4, max=13)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    national_id = StringField('National ID', validators=[DataRequired(), Length(max=16)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Update Profile')
