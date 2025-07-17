from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired


class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    semester_id = SelectField('Semester', coerce=int, validators=[DataRequired()])
    enrollment_date = DateField('Enrollment Date', validators=[DataRequired()], format='%Y-%m-%d')
    grade = StringField('Grade')
    submit = SubmitField('Save Enrollment')