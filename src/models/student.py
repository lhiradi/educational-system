from src.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.students_courses import StudentsCourses

class Student(db.Model, UserMixin):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(13), nullable=False, unique=True)
    national_id = db.Column(db.String(10), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    unit = db.Column(db.Integer, default=0)
    course_links = db.relationship(
        'StudentsCourses',
        back_populates='student',
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)