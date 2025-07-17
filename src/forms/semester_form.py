from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

class SemesterForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2020, max=2100)])
    term = StringField('Term (e.g., Fall, Spring)', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save Semester')

    def validate_end_date(self, field):
        if self.start_date.data and field.data < self.start_date.data:
            raise ValidationError('End date must not be earlier than start date.')