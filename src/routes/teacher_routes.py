from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from src.extensions import teacher_required, db
from src.utils.logger import Logger
from src.models.student import Student
from src.models.course import Course
from src.models.teacher import Teacher
from src.models.students_courses import StudentsCourses

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")
logger = Logger("teacher_app")

@teacher_bp.route("/")
@login_required
@teacher_required
def teacher_home():
    logger.info(f"Teacher {current_user.teacher_id} accessed the teacher dashboard.")
    return render_template("teacher/home.html", teacher=current_user)

@teacher_bp.route("/courses")
@login_required
@teacher_required
def show_courses():
    try:
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
        logger.info(f"Teacher {current_user.teacher_id} viewed their courses.")
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching courses for teacher {current_user.teacher_id}: {e}")
        flash("A database error occurred while fetching your courses.", "danger")
        courses = []
    return render_template("teacher/courses.html", courses=courses)

@teacher_bp.route("/students")
@login_required
@teacher_required
def show_students():
    try:
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
        students = [StudentsCourses.query.options(joinedload(StudentsCourses.student)).filter_by(course_id=course.id).all() for course in courses]
        student_courses = zip(courses, students)
        logger.info(f"Teacher {current_user.teacher_id} viewed their student list.")
        return render_template("teacher/students.html", student_courses=student_courses, courses=courses)
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching students for teacher {current_user.teacher_id}: {e}")
        flash("A database error occurred while fetching your students.", "danger")
        return render_template("teacher/students.html", student_courses=[], courses=[])

@teacher_bp.route("/student/<int:student_id>/<int:course_id>/delete", methods=["POST", "GET"])
@login_required
@teacher_required
def delete_student(student_id, course_id):
    student = Student.query.get_or_404(student_id)
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()

    if request.method == "POST":
        try:
            db.session.delete(enrollment)
            db.session.commit()
            logger.info(f"Teacher {current_user.teacher_id} deleted student {student_id} from course {course_id}.")
            flash(f"{student.first_name} {student.last_name} was successfully removed from the course.", "success")
            return redirect(url_for("teacher.show_students"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during student deletion by teacher {current_user.teacher_id}: {e}")
            flash("A database error occurred. The student could not be removed.", "danger")
            return redirect(url_for("teacher.show_students"))

    return render_template("teacher/delete_student.html", student=student)

@teacher_bp.route("/student/<int:student_id>/<int:course_id>/edit/score", methods=["POST", "GET"])
@login_required
@teacher_required
def edit_score(student_id, course_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
    if request.method == "POST":
        try:
            enrollment.grade = request.form["grade"]
            db.session.commit()
            logger.info(f"Teacher {current_user.teacher_id} updated grade for student {student_id} in course {course_id}.")
            flash("Grade updated successfully!", "success")
            return redirect(url_for("teacher.show_students"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during grade update by teacher {current_user.teacher_id}: {e}")
            flash("A database error occurred. The grade was not updated.", "danger")

    return render_template("teacher/edit_score.html", enrollment=enrollment)