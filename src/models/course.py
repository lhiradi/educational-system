from src.extensions import db
from src.models.students_courses import StudentsCourses

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(8), nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False, default=2)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    capacity = db.Column(db.Integer, default=30)
    student_links = db.relationship(
        'StudentsCourses',
        back_populates='course'
    )
    teacher = db.relationship("Teacher", back_populates="courses")