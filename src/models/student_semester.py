from src.extensions import db

class StudentSemester(db.Model):
    __tablename__ = 'student_semesters'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), primary_key=True)
    is_finalized = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', back_populates='semester_links')
    semester = db.relationship('Semester', back_populates='student_links')