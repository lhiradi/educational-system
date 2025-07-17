from src.models.semester import Semester
from datetime import date
def days_overlap(days1, days2):
    set1 = set(day.strip().upper() for day in days1.split(","))
    set2 = set(day.strip().upper() for day in days2.split(","))
    return not set1.isdisjoint(set2)

def get_total_enrolled_units(student, semester_id):
    """Returns the sum of units for all courses the student is enrolled in for a specific semester."""
    return sum(link.course.course_unit for link in student.course_links if link.semester_id == semester_id)

def get_current_semester():
    today = date.today()
    return Semester.query.filter(Semester.start_date <= today, Semester.end_date >= today).first()