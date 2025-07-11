from flask import request, redirect, url_for, flash
from flask import Blueprint, render_template
from src.utils.logger import Logger
from sqlalchemy.exc import SQLAlchemyError
from src.models.student import Student
from src.models.course import Course
from src.models.students_courses import StudentsCourses
from src.extensions import db, student_required
from src.utils import days_overlap, get_total_enrolled_units
from flask_login import login_required, current_user
from datetime import date
from src.models.setting import Setting

student_bp = Blueprint("student", __name__, url_prefix="/student")
logger = Logger("student_app")

@student_bp.route("/")
@login_required
@student_required
def home():
    logger.info(f"Student {current_user.student_id} accessed their home page.")
    return render_template("student/home.html")

@student_bp.route("/courses")
@login_required
@student_required
def show_courses():
    try:
        course_links = current_user.course_links
        enrolled_courses = [link.course for link in course_links]
        grades = [link.grade for link in course_links]
        teachers = [f"{c.teacher.first_name} {c.teacher.last_name}" if c.teacher else "N/A" for c in enrolled_courses]
        courses_info = zip(enrolled_courses, grades, teachers)

        all_courses = Course.query.all()
        enrolled_course_ids = {course.id for course in enrolled_courses}
        available_courses = [course for course in all_courses if course.id not in enrolled_course_ids]

        logger.info(f"Student {current_user.student_id} viewed their courses.")
        return render_template("student/show_courses.html", courses_info=courses_info, available_courses=available_courses)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching courses for student {current_user.student_id}: {e}")
        flash("A database error occurred while fetching your courses.", "danger")
        return render_template("student/show_courses.html", courses_info=[], available_courses=[])




@student_bp.route("/enroll", methods=["POST"])
@login_required
@student_required
def enroll_course():
    course_id = request.form.get("course_id")
    if not course_id:
        flash("No course selected for enrollment.", "error")
        return redirect(url_for("student.show_courses"))

    try:
        course_to_enroll = Course.query.get(course_id)
        if not course_to_enroll:
            flash("Selected course does not exist.", "error")
            return redirect(url_for("student.show_courses"))

        enrolled_courses = [link.course for link in current_user.course_links]
        for enrolled_course in enrolled_courses:
            if days_overlap(enrolled_course.days, course_to_enroll.days) and \
               (enrolled_course.start_time < course_to_enroll.end_time and
                course_to_enroll.start_time < enrolled_course.end_time):
                flash(f"Time conflict with course: {enrolled_course.course_name}", "error")
                return redirect(url_for("student.show_courses"))

        setting = Setting.query.first()
        if not setting or not setting.enrollment_open:
            flash("Enrollment is currently closed.", "error")
            return redirect(url_for("student.show_courses"))

        if get_total_enrolled_units(current_user) + course_to_enroll.course_unit > 24:
            flash("You cannot enroll in this course because your total units will exceed 24.", "error")
            return redirect(url_for("student.show_courses"))

        if len(course_to_enroll.student_links) >= course_to_enroll.capacity:
            flash("This course is full and cannot accept more students.", "error")
            return redirect(url_for("student.show_courses"))

        new_link = StudentsCourses(student_id=current_user.id, course_id=course_to_enroll.id, enrollment_date=date.today())
        db.session.add(new_link)
        db.session.commit()

        logger.info(f"Student {current_user.student_id} successfully enrolled in course {course_to_enroll.course_name}.")
        flash(f"Successfully enrolled in {course_to_enroll.course_name}.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error during enrollment for student {current_user.student_id}: {e}")
        flash("A database error occurred. Please try again.", "danger")

    return redirect(url_for("student.show_courses"))

@student_bp.route("/finalize", methods=["POST"])
@login_required
@student_required
def finalize_enrollment():
    total_units = get_total_enrolled_units(current_user)
    if total_units < 14:
        flash("You must enroll in at least 14 units to finalize enrollment.", "error")
        return redirect(url_for("student.show_courses"))
    if total_units > 24:
        flash("You cannot finalize enrollment with more than 24 units.", "error")
        return redirect(url_for("student.show_courses"))

    logger.info(f"Student {current_user.student_id} finalized their enrollment with {total_units} units.")
    flash("Enrollment finalized successfully!", "success")
    return redirect(url_for("student.show_courses"))
