from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, DateField,
    IntegerField, TimeField, BooleanField, TextAreaField, HiddenField
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class CourseForm(FlaskForm):
    course_id = StringField('Course ID', validators=[DataRequired(), Length(max=16)])
    course_name = StringField('Course Name', validators=[DataRequired(), Length(max=128)])
    course_unit = IntegerField('Units', validators=[DataRequired(), NumberRange(min=1, max=6)])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    days = StringField('Days (e.g. Mon,Wed)', validators=[DataRequired(), Length(max=32)])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Course')