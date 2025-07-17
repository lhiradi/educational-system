from src.extensions import db

class Semester(db.Model):
    __tablename__ = "semesters"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    term = db.Column(db.String(10), nullable=False)  
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    student_links = db.relationship('StudentSemester', back_populates='semester', cascade="all, delete-orphan")

    