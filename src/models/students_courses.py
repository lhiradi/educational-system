from src.extensions import db

class StudentsCourses(db.Model):
    __tablename__ = 'students_courses'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), primary_key=True)
    enrollment_date = db.Column(db.Date)
    grade = db.Column(db.String(2))

    student = db.relationship('Student', back_populates='course_links')
    course = db.relationship('Course', back_populates='student_links')
    semester = db.relationship("Semester", back_populates='course_links')