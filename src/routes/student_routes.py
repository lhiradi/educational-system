from flask import Blueprint, render_template
from src.models.student import Student
from flask_login import login_required
student_bp = Blueprint("student", __name__, url_prefix="stu")

@student_bp.route("/<int:id>/profile")
@login_required
def show_profile(id):
    student = Student.query.get_or_404(id)
    courses = [link.course for link in student.course_links]
    grades = [link.grade for link in student.course_links]
    return render_template("student_profile.html", student=student, courses=courses, grades=grades)