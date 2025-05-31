from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import joinedload
import datetime
from flask_login import login_required, current_user
from src.extensions import teacher_required, db
from src.models.student import Student
from src.models.course import Course
from src.models.teacher import Teacher
from src.models.students_courses import StudentsCourses

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_bp.route("/")
@login_required
@teacher_required
def teacher_home():
    return render_template("teacher/home.html", teacher=current_user)

@teacher_bp.route("/courses")
@login_required
@teacher_required
def show_courses():
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template("teacher/courses.html", courses=courses)

@teacher_bp.route("/students")
@login_required
@teacher_required
def show_students():
   courses = Course.query.filter_by(teacher_id=current_user.id).all()
   students = [StudentsCourses.query.options(joinedload(StudentsCourses.student)).filter_by(course_id=course.id).all() for course in courses]
   student_courses = zip(courses, students)
   return render_template("teacher/students.html", student_courses=student_courses, courses=courses)
   
@teacher_bp.route("/student/<int:id>/delete", methods=["POST", "GET"])
@login_required
@teacher_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(student)
        db.session.commit()
        flash(f"{student.first_name} {student.last_name} deleted from selected course.")
        return redirect(url_for("teacher.teacher_home"))
    return render_template("teacher/delete_student.html", student=student)

@teacher_bp.route("/student/<int:student_id>/<int:course_id>/edit/score", methods=["POST", "GET"])
@login_required
@teacher_required
def edit_score(student_id, course_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id).first()
    if request.method == "POST":
        enrollment.grade = request.form["grade"]
        db.session.commit()
        flash("Grade updated")
        return redirect(url_for("teacher.teacher_home"))
    return render_template("teacher/edit_score.html", enrollment=enrollment)