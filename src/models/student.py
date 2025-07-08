from src.extensions import db
from src.models.base_model import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.students_courses import StudentsCourses

class Student(BaseModel, UserMixin):
    __tablename__ = "students"
    
    student_id = db.Column(db.String(13), nullable=False, unique=True)
    unit = db.Column(db.Integer, default=0)
    course_links = db.relationship(
        'StudentsCourses',
        back_populates='student',
        cascade="all, delete-orphan"
    )

    @property
    def user_type(self):
        
        return "student"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    