from flask import request, redirect, url_for, flash
from flask import Blueprint, render_template
from src.utils.logger import Logger
from sqlalchemy.exc import SQLAlchemyError
from src.models.student import Student
from src.models.course import Course
from src.models.students_courses import StudentsCourses
from src.models.student_semester import StudentSemester
from src.models.semester import Semester
from src.extensions import db, student_required
from src.utils import days_overlap, get_total_enrolled_units, get_current_semester, time_overlap
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
        current_semester = get_current_semester()
        is_current_semester_finalized = False
        
        if not current_semester:
            flash("There is no active semester at the moment", "danger")
            return render_template("student/show_courses.html", courses_info=[], available_courses=[], 
                                   current_semester=None, is_current_semester_finalized=is_current_semester_finalized)
        
        course_links = StudentsCourses.query.filter_by(student_id=current_user.id, semester_id=current_semester.id).all()
        enrolled_courses = [link.course for link in course_links]
        grades = [link.grade for link in course_links]
        teachers = [f"{c.teacher.first_name} {c.teacher.last_name}" if c.teacher else "N/A" for c in enrolled_courses]
        courses_info = zip(enrolled_courses, grades, teachers)
        
        all_courses = Course.query.all()
        enrolled_course_ids = {course.id for course in enrolled_courses}
        available_courses = [course for course in all_courses if course.id not in enrolled_course_ids]

        current_semester_status = StudentSemester.query.filter_by(student_id=current_user.id, semester_id=current_semester.id).first()
        if current_semester_status and current_semester_status.is_finalized:
            is_current_semester_finalized = True
            
        setting = Setting.query.first()
        is_enrollment_open = setting.enrollment_open if setting else False 
        
        logger.info(f"Student {current_user.student_id} viewed their courses.")
        return render_template("student/show_courses.html", courses_info=courses_info, 
                               available_courses=available_courses, current_semester=current_semester, 
                               is_current_semester_finalized=is_current_semester_finalized,
                               is_enrollment_open=is_enrollment_open)
        
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching courses for student {current_user.student_id}: {e}")
        flash("A database error occurred while fetching your courses.", "danger")
        return render_template("student/show_courses.html", courses_info=[], available_courses=[], current_semester=None,
                               is_current_semester_finalized=False,
                               is_enrollment_open=is_enrollment_open)




@student_bp.route("/enroll", methods=["POST"])
@login_required
@student_required
def enroll_course():
    current_semester = get_current_semester()
    if not current_semester:
        flash("Enrollment is not open at the moment.", "error")
        return redirect(url_for("student.show_courses"))
    
    student_semester_status = StudentSemester.query.filter_by(student_id=current_user.id, semester_id=current_semester.id).first()
    if student_semester_status and student_semester_status.is_finalized:
        flash("You have already finalized your enrollment and cannot make changes.", "error")
        return redirect(url_for("student.show_courses"))
    
    course_id = request.form.get("course_id")
    if not course_id:
        flash("No course selected for enrollment.", "error")
        return redirect(url_for("student.show_courses"))

    try:
        course_to_enroll = Course.query.get(course_id)
        if not course_to_enroll:
            flash("Selected course does not exist.", "error")
            return redirect(url_for("student.show_courses"))

        enrolled_courses_links = StudentsCourses.query.filter_by(student_id=current_user.id, semester_id=current_semester.id).all()
        enrolled_courses = [link.course for link in enrolled_courses_links]
        for enrolled_course in enrolled_courses:
            if days_overlap(enrolled_course.days, course_to_enroll.days) and \
               time_overlap(course_to_enroll, enrolled_course):
                flash(f"Time conflict with course: {enrolled_course.course_name}", "error")
                return redirect(url_for("student.show_courses"))

        setting = Setting.query.first()
        if not setting or not setting.enrollment_open:
            flash("Enrollment is currently closed.", "error")
            return redirect(url_for("student.show_courses"))

        if get_total_enrolled_units(current_user, current_semester.id) + course_to_enroll.course_unit > 24:
            flash("You cannot enroll in this course because your total units will exceed 24.", "error")
            return redirect(url_for("student.show_courses"))

        if len(course_to_enroll.student_links) >= course_to_enroll.capacity:
            flash("This course is full and cannot accept more students.", "error")
            return redirect(url_for("student.show_courses"))

        new_link = StudentsCourses(student_id=current_user.id, course_id=course_to_enroll.id, semester_id=current_semester.id ,enrollment_date=date.today())
        db.session.add(new_link)
        
        student_semester = StudentSemester.query.filter_by(student_id=current_user.id, semester_id=current_semester.id).first()
        if not student_semester:
            student_semester = StudentSemester(student_id=current_user.id, semester_id=current_semester.id)
            db.session.add(student_semester)
        
        db.session.commit()

        logger.info(f"Student {current_user.student_id} successfully enrolled in course {course_to_enroll.course_name} for semester {current_semester.year}, {current_semester.term}.")
        flash(f"Successfully enrolled in {course_to_enroll.course_name}.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error during enrollment for student {current_user.student_id}: {e}")
        flash("A database error occurred. Please try again.", "danger")

    return redirect(url_for("student.show_courses"))

@login_required
@student_required
@student_bp.route("/unenroll/<int:course_id>")
def unenroll(course_id):
    try:
        current_semester = get_current_semester()
        enrollment = StudentsCourses.query.filter_by(course_id=course_id, semester_id=current_semester.id, student_id=current_user.id).first()
        db.session.delete(enrollment)
        db.session.commit()
        flash("Course unenrolled successfully", "success")
        logger.info(f"Student {current_user.student_id} successfully unenrolled in course {course_id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("A database error occurred. Please try again.", "danger")
        logger.error(f"Database error during unenrolling student {current_user.student_id}: {e}")
    return redirect(url_for("student.show_courses"))
   
@student_bp.route("/finalize", methods=["POST"])
@login_required
@student_required
def finalize_enrollment():
    current_semester = get_current_semester()
    if not current_semester:
        flash("Cannot finalize enrollment, no active semester.", "error")
        return redirect(url_for("student.show_courses"))

    total_units = get_total_enrolled_units(current_user, current_semester.id)
    if total_units < 14:
        flash("You must enroll in at least 14 units to finalize enrollment.", "error")
        return redirect(url_for("student.show_courses"))
    if total_units > 24:
        flash("You cannot finalize enrollment with more than 24 units.", "error")
        return redirect(url_for("student.show_courses"))

    student_semester = StudentSemester.query.filter_by(student_id=current_user.id, semester_id=current_semester.id).first()
    if student_semester:
        student_semester.is_finalized = True
        db.session.commit()
        logger.info(f"Student {current_user.student_id} finalized their enrollment for semester {current_semester.id} with {total_units} units.")
        flash("Enrollment finalized successfully!", "success")
    else:
        flash("Could not find semester enrollment to finalize.", "error")

    return redirect(url_for("student.show_courses"))

@student_bp.route("/history")
@login_required
@student_required
def semester_history():
    try:
        student_semesters = StudentSemester.query.filter_by(student_id=current_user.id).all()
        semesters = [ss.semester for ss in student_semesters]
        logger.info(f"Student {current_user.student_id} viewed their semester history.")
        return render_template("student/semester_history.html", semesters=semesters)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching semester history for student {current_user.student_id}: {e}")
        flash("A database error occurred while fetching your semester history.", "danger")
        return render_template("student/semester_history.html", semesters=[])


@student_bp.route("/semester/<int:semester_id>")
@login_required
@student_required
def semester_details(semester_id):
    try:
        semester = Semester.query.get_or_404(semester_id)
        course_links = StudentsCourses.query.filter_by(student_id=current_user.id, semester_id=semester_id).all()
        courses_info = []
        for link in course_links:
            teacher = f"{link.course.teacher.first_name} {link.course.teacher.last_name}" if link.course.teacher else "N/A"
            courses_info.append((link.course, link.grade, teacher))

        logger.info(f"Student {current_user.student_id} viewed details for semester {semester_id}.")
        return render_template("student/semester_details.html", courses_info=courses_info, semester=semester)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching semester details for student {current_user.student_id}: {e}")
        flash("A database error occurred while fetching semester details.", "danger")
        return redirect(url_for('student.semester_history'))