from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=13)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Login')
    
class IDForm(FlaskForm):
    user_id = StringField('Student/Teacher ID', validators=[DataRequired()])
    submit = SubmitField('Send OTP')

class OTPLoginForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Login')