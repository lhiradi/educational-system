from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from src.extensions import teacher_required, db
from src.utils.logger import Logger
from src.utils import get_current_semester
from src.models.student import Student
from src.models.course import Course
from src.models.teacher import Teacher
from src.models.semester import Semester
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
        page = request.args.get("page", 1, type=int)
        courses = Course.query.filter_by(teacher_id=current_user.id).paginate(page=page, per_page=10)
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

@teacher_bp.route("/student/<int:student_id>/<int:course_id>/<int:semester_id>/delete", methods=["POST", "GET"])
@login_required
@teacher_required
def delete_student(student_id, course_id, semester_id):
    student = Student.query.get_or_404(student_id)
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id, semester_id=semester_id).first_or_404()

    if request.method == "POST":
        try:
            db.session.delete(enrollment)
            db.session.commit()
            logger.info(f"Teacher {current_user.teacher_id} deleted student {student_id} from course {course_id} in semester {semester_id}.")
            flash(f"{student.first_name} {student.last_name} was successfully removed from the course.", "success")
            return redirect(url_for("teacher.show_students"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during student deletion by teacher {current_user.teacher_id}: {e}")
            flash("A database error occurred. The student could not be removed.", "danger")
            return redirect(url_for("teacher.show_students"))

    return render_template("teacher/delete_student.html", student=student)


@teacher_bp.route("/student/<int:student_id>/<int:course_id>/<int:semester_id>/edit/score", methods=["POST", "GET"])
@login_required
@teacher_required
def edit_score(student_id, course_id, semester_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id, semester_id=semester_id).first_or_404()
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

@teacher_bp.route("/history")
@login_required
@teacher_required
def semester_history():

    try:
        teacher = Teacher.query.filter_by(national_id=current_user.national_id).first()
        if not teacher:
            logger.error(f"Teacher record not found for user {current_user.national_id}")
            flash("Teacher record not found.", "danger")
            return render_template("teacher/semester_history.html", semesters=[])

        semesters = db.session.query(Semester)\
                              .join(StudentsCourses, Semester.id == StudentsCourses.semester_id) \
                              .join(Course, StudentsCourses.course_id == Course.id) \
                              .filter(Course.teacher_id == teacher.id) \
                              .distinct(Semester.id) \
                              .order_by(Semester.start_date.desc()) \
                              .all()

        logger.info(f"Teacher {getattr(teacher, 'teacher_id', 'Unknown ID')} viewed their semester history.")
        return render_template("teacher/semester_history.html", semesters=semesters)

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while fetching semester history for teacher {getattr(current_user, 'teacher_id', 'Unknown')}: {e}")
        flash("A database error occurred while fetching your semester history.", "danger")
        return render_template("teacher/semester_history.html", semesters=[])


@teacher_bp.route("/semester/<int:semester_id>")
@login_required
@teacher_required
def semester_details(semester_id):
    try:
        teacher = Teacher.query.filter_by(national_id=current_user.national_id).first()
        if not teacher:
             logger.error(f"Teacher record not found for user {current_user.national_id}")
             flash("Teacher record not found.", "danger")
             return redirect(url_for('teacher.semester_history'))

        semester = Semester.query.get_or_404(semester_id)
        courses = db.session.query(Course)\
                            .join(StudentsCourses, Course.id == StudentsCourses.course_id) \
                            .filter(Course.teacher_id == teacher.id, StudentsCourses.semester_id == semester_id) \
                            .distinct(Course.id) \
                            .all()

        logger.info(f"Teacher {getattr(teacher, 'teacher_id', 'Unknown ID')} viewed details for semester {semester_id}.")
        return render_template("teacher/semester_details.html", courses=courses, semester=semester)

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while fetching semester details for teacher {getattr(current_user, 'teacher_id', 'Unknown')}, semester {semester_id}: {e}")
        flash("A database error occurred while fetching semester details.", "danger")
        return redirect(url_for('teacher.semester_history'))