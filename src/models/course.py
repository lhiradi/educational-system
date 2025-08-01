from src.extensions import db
from src.models.students_courses import StudentsCourses

VALID_DAYS = ["SATURDAY", "SUNDAY", "MONDAY",
              "TUESDAY", "WEDNESDAY", "THURSDAY"]

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(8), nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False, default=2)
    capacity = db.Column(db.Integer, default=30)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    days = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
        
    student_links = db.relationship(
        'StudentsCourses',
        back_populates='course',
        cascade="all, delete-orphan"
    )
    teacher = db.relationship("Teacher", back_populates="courses")
    
    @db.validates("days")
    def validate_days(self, key, value):
        input_days = [day.strip().upper() for day in value.split(",")]
        for day in input_days:
            if day not in VALID_DAYS:
                raise ValueError(f"Invalid day: {day}")
            
        return ",".join(input_days)