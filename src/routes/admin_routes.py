from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import joinedload
import datetime
from flask_login import login_required
from src.extensions import admin_required
from src.models.student import Student
from src.models.course import Course
from src.models.teacher import Teacher
from src.models.students_courses import StudentsCourses
from src.extensions import db
from src.models.setting import Setting

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@login_required
@admin_required
def home():
    setting = Setting.query.first()
    return render_template("admin/home.html", setting=setting)

@admin_bp.route("/students")
@login_required
@admin_required
def show_students():
    students = Student.query.all()
    return render_template("admin/students.html", students=students)

@admin_bp.route("/create/student", methods=["POST", "GET"])
@login_required
@admin_required
def create_student():
    if request.method == "POST":
        student = Student()
        student.first_name = request.form["first_name"]
        student.last_name = request.form["last_name"]
        student.student_id = request.form["student_id"]
        student.date_of_birth = datetime.datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d").date()
        student.national_id = request.form["national_id"]
        student.set_password(request.form["password"])
        db.session.add(student)
        db.session.commit()
        flash("User created!")
        return redirect(url_for("admin.home"))
    return render_template("admin/create_student.html")


@admin_bp.route("/student/<int:id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted!")
        return redirect(url_for("admin.home"))
    return render_template("admin/delete_student.html", student=student) 
   
@admin_bp.route("/student/<int:id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        student.first_name = request.form["first_name"]
        student.last_name = request.form["last_name"]
        student.national_id = request.form["national_id"]
        student.date_of_birth = datetime.datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d").date()
        db.session.commit()
        flash("User updated successfully!")
        return redirect(url_for("admin.home"))
    return render_template("admin/edit_student.html", student=student)



@admin_bp.route("/courses")
@login_required
@admin_required
def show_courses():
    courses = Course.query.options(joinedload(Course.teacher)).all()
    return render_template("admin/courses.html", courses=courses)

@admin_bp.route("/create/course", methods=["POST", "GET"])
@login_required
@admin_required
def create_course():
    if request.method == "POST":
        course = Course()
        course.course_id = request.form["course_id"]
        course.course_name = request.form["course_name"]
        course.course_unit = request.form["course_unit"]
        course.teacher_id = request.form["teacher_id"]
        course.capacity = request.form["capacity"]
        course.start_date = datetime.datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        course.end_date = datetime.datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        course.days = request.form["days"]
        course.start_time = datetime.datetime.strptime(request.form["start_time"], "%H:%M").time()
        course.end_time = datetime.datetime.strptime(request.form["end_time"], "%H:%M").time()
        db.session.add(course)
        db.session.commit()
        flash(f"{course.course_id} added!")
        return redirect(url_for("admin.home"))
    teachers = Teacher.query.all()
    return render_template("admin/create_course.html", teachers=teachers)

@admin_bp.route("/course/<int:id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    teachers = Teacher.query.all()
    if request.method == "POST":
        course.course_id = request.form["course_id"]
        course.course_name = request.form["course_name"]
        course.course_unit = request.form["course_unit"]
        course.teacher_id = request.form["teacher_id"]
        course.capacity = request.form["capacity"]
        course.start_date = datetime.datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        course.end_date = datetime.datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        course.days = request.form["days"]
        course.start_time = datetime.datetime.strptime(request.form["start_time"], "%H:%M").time()
        course.end_time = datetime.datetime.strptime(request.form["end_time"], "%H:%M").time()
        db.session.commit()
        flash("Course updated!")
        return redirect(url_for("admin.home"))
    return render_template("admin/edit_course.html", course=course, teachers=teachers)

@admin_bp.route("/course/<int:id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    if request.method == "POST":
        from src.models.students_courses import StudentsCourses
        enrollments = StudentsCourses.query.filter_by(course_id=course.id).all()
        for enrollment in enrollments:
            db.session.delete(enrollment)
            
        db.session.delete(course)
        db.session.commit()
        flash(f"{course.course_id} deleted!")
        return redirect(url_for("admin.home"))
    return render_template("admin/delete_course.html", course=course)

@admin_bp.route("/teachers")
@login_required
@admin_required
def show_teachers():
    teachers = Teacher.query.all()
    return render_template("admin/teachers.html", teachers=teachers)

@admin_bp.route("/teacher/create", methods=["POST", "GET"])
@login_required
@admin_required
def create_teacher():
    if request.method == "POST":
        teacher = Teacher()
        teacher.first_name = request.form["first_name"]
        teacher.last_name = request.form["last_name"]
        teacher.teacher_id = request.form["teacher_id"]
        teacher.date_of_birth = datetime.datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d").date()
        teacher.national_id = request.form["national_id"]
        teacher.set_password(request.form["password"])
        db.session.add(teacher)
        db.session.commit()
        flash("Teacher created!")
        return redirect(url_for("admin.home"))
    return render_template("admin/create_teacher.html")

@admin_bp.route("/teacher/<int:id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    if request.method == "POST":
        teacher.first_name = request.form["first_name"]
        teacher.last_name = request.form["last_name"]
        teacher.national_id = request.form["national_id"]
        teacher.date_of_birth = datetime.datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d").date()
        db.session.commit()
        flash("Teacher updated successfully!")
        return redirect(url_for("admin.home"))
    return render_template("admin/edit_teacher.html", teacher=teacher)

@admin_bp.route("/teacher/<int:id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(teacher)
        db.session.commit()
        flash("Teacher deleted!")
        return redirect(url_for("admin.home"))
    return render_template("admin/delete_teacher.html", teacher=teacher)

@admin_bp.route("/enrollments")
@login_required
@admin_required
def show_enrollments():
    enrollments = StudentsCourses.query.join(StudentsCourses.student).join(StudentsCourses.course).all()
    return render_template("admin/enrollments.html", enrollments=enrollments)

@admin_bp.route("/enrollment/create", methods=["POST", "GET"])
@login_required
@admin_required
def add_enrollment():
    if request.method == "POST":
        enrollment =  StudentsCourses()
        enrollment.course_id = request.form["course_id"]
        enrollment.student_id = request.form["student_id"]
        enrollment.enrollment_date = datetime.datetime.strptime(request.form["enrollment_date"], "%Y-%m-%d").date()
        enrollment.grade = request.form["grade"]
        db.session.add(enrollment)
        db.session.commit()
        flash("Enrollment created successfully")
        return redirect(url_for("admin.home"))
    students = Student.query.all()
    courses = Course.query.all()
    return render_template("admin/create_enrollment.html", students=students, courses=courses)

@admin_bp.route("/enrollment/<int:student_id>/<int:course_id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_enrollment(student_id, course_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
    if request.method == "POST":
        enrollment.course_id = request.form["course_id"]
        enrollment.student_id = request.form["student_id"]
        enrollment.enrollment_date = datetime.datetime.strptime(request.form["enrollment_date"], "%Y-%m-%d").date()
        enrollment.grade = request.form["grade"]
        db.session.commit()
        flash("Enrollment updated!")
        return redirect(url_for("admin.home"))
    
    students = Student.query.all()
    courses = Course.query.all()
    return render_template("admin/edit_enrollment.html", students=students, courses=courses, enrollment=enrollment)

@admin_bp.route("/enrollment/<int:student_id>/<int:course_id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_enrollment(student_id, course_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
    if request.method == "POST":
        db.session.delete(enrollment)
        db.session.commit()
        flash("Enrollment deleted successfully!")
        return redirect(url_for("admin.show_enrollments"))
    return render_template("admin/delete_enrollment.html", enrollment=enrollment)

@admin_bp.route("/toggle-enrollment", methods=["POST"])
@login_required
@admin_required
def toggle_enrollment():
    setting = Setting.query.first()
    setting.enrollment_open = not setting.enrollment_open
    db.session.commit()
    flash(f"Enrollment is now {'open' if setting.enrollment_open else 'closed'}.")
    return redirect(url_for("admin.home"))
