from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, DateField,
    IntegerField, TimeField, BooleanField, TextAreaField, HiddenField
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=13)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Login')