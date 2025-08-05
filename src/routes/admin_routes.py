from flask import Blueprint, render_template, request, flash, redirect, url_for 
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_login import login_required, current_user
from src.extensions import admin_required
from src.models.student import Student
from src.models.course import Course
from src.models.teacher import Teacher
from src.models.semester import Semester
from src.models.post import Post
from src.forms.student_form import StudentForm, StudentProfileForm
from src.forms.course_form import CourseForm
from src.forms.semester_form import SemesterForm
from src.models.student_semester import StudentSemester
from src.forms.teacher_form import TeacherForm, TeacherProfileForm
from src.forms.enrollment_form import EnrollmentForm
from src.forms.post_form import PostForm
from src.models.students_courses import StudentsCourses
from src.extensions import db
from src.models.setting import Setting
from src.utils.logger import Logger

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
logger = Logger("admin_app") 

@admin_bp.route("/")
@login_required
@admin_required
def home():
    setting = Setting.query.first()
    logger.info("Admin accessed the admin dashboard.")
    return render_template("admin/home.html", setting=setting)

@admin_bp.route("/students")
@login_required
@admin_required
def show_students():
    logger.info("Admin visited the students page.")
    try:
        page = request.args.get("page", 1, type=int)
        students = Student.query.paginate(page=page, per_page=10)
    except SQLAlchemyError as e:
        logger.error(f"Database error during fetching students: {e}")
        flash("A database error occurred while fetching students.", "danger")
        students = []
    return render_template("admin/students.html", students=students)

@admin_bp.route("/create/student", methods=["POST", "GET"])
@login_required
@admin_required
def create_student():
    form = StudentForm()
    if form.validate_on_submit():
        try:
            student = Student()
            student.first_name = form.first_name.data
            student.last_name = form.last_name.data
            student.student_id = form.student_id.data
            student.email = form.email.data
            student.date_of_birth = form.date_of_birth.data 
            student.national_id = form.national_id.data
            student.set_password(form.password.data)
            db.session.add(student)
            db.session.commit()
            logger.info(f"Student {student.student_id} registered bt admin.")
            flash("Student created!", "success")
            return redirect(url_for("admin.home"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to create student. {student.student_id} already exists.")
            flash("Student with that ID already exists", "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during student creation by admin: {e}")
            flash("A database error occurred. Please try again.", "danger")
    return render_template("admin/create_student.html", form=form)


@admin_bp.route("/student/<int:id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
       try:
            db.session.delete(student)
            db.session.commit()
            logger.info(f"Student with ID {student.student_id} deleted by admin.")
            flash("Student deleted!", "success")
            return redirect(url_for("admin.home"))
       except SQLAlchemyError as e:
           db.session.rollback()
           logger.error(f"Database error during student deletion by admin for student ID {student.student_id}: {e}")
           flash("Database error occured, please try again.", "danger")
           return(redirect(url_for("admin.show_students")))
    
    return render_template("admin/delete_student.html", student=student) 
   
@admin_bp.route("/student/<int:id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentProfileForm(obj=student)
    if form.validate_on_submit():
        try:
            student.first_name = form.first_name.data
            student.last_name = form.last_name.data
            student.email = form.email.data
            student.national_id = form.national_id.data
            student.date_of_birth = form.date_of_birth.data
            db.session.commit()
            logger.info(f"Student with ID {student.student_id} updated.")
            flash("User updated successfully!", "success")
            return redirect(url_for("admin.show_students"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to update student {student.student_id} .Student ID {form.student_id.data} already exists.")
            flash("A student with that ID already exists.", "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error occured during student update by admin for student {student.student_id}: {e}")
            flash("Database error occured, please try again", "danger")
            
    return render_template("admin/edit_student.html", student=student, form=form)



@admin_bp.route("/courses")
@login_required
@admin_required
def show_courses():
    logger.info("Admin accessed courses page.")
    try:
        page = request.args.get("page", 1, type=int)
        courses = Course.query.options(joinedload(Course.teacher), joinedload(Course.prerequisite)).paginate(page=page, per_page=10)
    except SQLAlchemyError as e:
        logger.error(f"Database error occured while fetching courses: {e}")
        flash("A database error occurred while fetching courses.", "danger")
        courses = []
    return render_template("admin/courses.html", courses=courses)

@admin_bp.route("/create/course", methods=["POST", "GET"])
@login_required
@admin_required
def create_course():
    form = CourseForm()
    form.teacher_id.choices = [(t.id, f"{t.first_name} {t.last_name}") for t in Teacher.query.all()]
    form.prerequisite_id.choices = [(0, 'None')] + [(c.id, f"{c.course_name} ({c.course_id})") for c in Course.query.all()]
    
    if form.validate_on_submit():
        try:
            course = Course()
            course.course_id = form.course_id.data
            course.course_name = form.course_name.data
            course.course_unit = form.course_unit.data
            course.capacity = form.capacity.data
            course.days = form.days.data
            course.start_date = form.start_date.data
            course.end_date = form.end_date.data
            course.start_time = form.start_time.data
            course.end_time = form.end_time.data
            course.teacher_id = form.teacher_id.data
            prerequisite_id = form.prerequisite_id.data
            course.prerequisite_id = prerequisite_id if prerequisite_id != 0 else None
            db.session.add(course)
            db.session.commit()
            logger.info(f"Course {course.course_id} created by admin.")
            flash(f"{course.course_id} added!", "success")
            return redirect(url_for("admin.home"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to create course. {form.course_id.data} already exists.")
            flash("A course with that ID already exists.", "danger")
        except ValueError as e:
            db.session.rollback()
            logger.warning(f"Admin failed to create course due to validation error: {e}")
            flash(str(e), "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during course creation by admin: {e}")
            flash("A database error occurred. Please try again.", "danger")

    return render_template("admin/create_course.html", form=form)

@admin_bp.route("/course/<int:id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    form.teacher_id.choices = [(t.id, f"{t.first_name} {t.last_name}") for t in Teacher.query.all()]
    form.prerequisite_id.choices = [(0, 'None')] + [(c.id, f"{c.course_name} ({c.course_id})") for c in Course.query.all() if c.id != course.id]
    
    if form.validate_on_submit():
        try:
            course.course_id = form.course_id.data
            course.course_name = form.course_name.data
            course.course_unit = form.course_unit.data
            course.capacity = form.capacity.data
            course.days = form.days.data
            course.start_time = form.start_time.data
            course.end_time = form.end_time.data
            course.start_date = form.start_date.data
            course.end_date = form.end_date.data
            course.teacher_id = form.teacher_id.data
            prerequisite_id = form.prerequisite_id.data
            course.prerequisite_id = prerequisite_id if prerequisite_id != 0 else None
            
            db.session.commit()
            logger.info(f"Course {course.course_id} updated by admin.")
            flash("Course updated!", "success")
            return redirect(url_for("admin.home"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to update course. {form.course_id.data} already exists.")
            flash("A course with that ID already exists.", "danger")
        except ValueError as e:
            db.session.rollback()
            logger.warning(f"Admin failed to update course {course.course_id} due to validation error: {e}")
            flash(str(e), "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during course update by admin for course {course.course_id}: {e}")
            flash("A database error occurred. Please try again.", "danger")

    return render_template("admin/edit_course.html", course=course, form=form)

@admin_bp.route("/course/<int:id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    if request.method == "POST":
        try:
            from src.models.students_courses import StudentsCourses
            enrollments = StudentsCourses.query.filter_by(course_id=course.id).all()
            for enrollment in enrollments:
                db.session.delete(enrollment)
                
            db.session.delete(course)
            db.session.commit()
            logger.info(f"Course {course.course_id} deleted by admin.")
            flash(f"{course.course_id} deleted!", "success")
            return redirect(url_for("admin.home"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during course deletion by admin for course {course.course_id}: {e}")
            flash("A database error occurred. Please try again.", "danger")
            return redirect(url_for("admin.show_courses"))

    return render_template("admin/delete_course.html", course=course)

@admin_bp.route("/teachers")
@login_required
@admin_required
def show_teachers():
    logger.info("Admin visited the teachers page.")
    try:
        page = request.args.get("page", 1, type=int)
        teachers = Teacher.query.paginate(page=page, per_page=10)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching teachers: {e}")
        flash("A database error occurred while fetching teachers.", "danger")
        teachers = []
    return render_template("admin/teachers.html", teachers=teachers)

@admin_bp.route("/teacher/create", methods=["POST", "GET"])
@login_required
@admin_required
def create_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        try:
            teacher = Teacher()
            teacher.teacher_id = form.teacher_id.data
            teacher.first_name = form.first_name.data
            teacher.last_name = form.last_name.data
            teacher.email = form.email.data
            teacher.national_id = form.national_id.data
            teacher.date_of_birth = form.date_of_birth.data
            teacher.set_password(form.password.data)
            db.session.add(teacher)
            db.session.commit()
            logger.info(f"Teacher {teacher.teacher_id} created by admin.")
            flash("Teacher created!", "success")
            return redirect(url_for("admin.home"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to create teacher. {form.teacher_id.data} already exists.")
            flash("A teacher with that ID already exists.", "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during teacher creation by admin: {e}")
            flash("A database error occurred. Please try again.", "danger")
    return render_template("admin/create_teacher.html", form=form)

@admin_bp.route("/teacher/<int:id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    form = TeacherProfileForm(obj=teacher)
    if form.validate_on_submit():
        try:
            teacher.teacher_id = form.teacher_id.data
            teacher.first_name = form.first_name.data
            teacher.last_name = form.last_name.data
            teacher.email = form.email.data
            teacher.national_id = form.national_id.data
            teacher.date_of_birth = form.date_of_birth.data
            db.session.commit()
            logger.info(f"Teacher {teacher.teacher_id} updated by admin.")
            flash("Teacher updated successfully!", "success")
            return redirect(url_for("admin.home"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to update teacher. {form.teacher_id.data} already exists.")
            flash("A teacher with that ID already exists.", "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during teacher update by admin for teacher {teacher.teacher_id}: {e}")
            flash("A database error occurred. Please try again.", "danger")
    return render_template("admin/edit_teacher.html", teacher=teacher, form=form)

@admin_bp.route("/teacher/<int:id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    if request.method == "POST":
        try:
            db.session.delete(teacher)
            db.session.commit()
            logger.info(f"Teacher {teacher.teacher_id} deleted by admin.")
            flash("Teacher deleted!", "success")
            return redirect(url_for("admin.home"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during teacher deletion by admin for teacher {teacher.teacher_id}: {e}")
            flash("A database error occurred. Please try again.", "danger")
            return redirect(url_for("admin.show_teachers"))

    return render_template("admin/delete_teacher.html", teacher=teacher)

@admin_bp.route("/enrollments")
@login_required
@admin_required
def show_enrollments():
    logger.info("Admin visited the enrollments page.")
    try:
        page = request.args.get("page", 1, type=int)
        enrollments = StudentsCourses.query.join(StudentsCourses.student).join(StudentsCourses.course).paginate(page=page, per_page=10)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching enrollments: {e}")
        flash("A database error occurred while fetching enrollments.", "danger")
        enrollments = []
    return render_template("admin/enrollments.html", enrollments=enrollments)

@admin_bp.route("/enrollment/create", methods=["POST", "GET"])
@login_required
@admin_required
def add_enrollment():
    form = EnrollmentForm()
    form.student_id.choices = [(s.id, f"{s.first_name} {s.last_name}") for s in Student.query.all()]
    form.course_id.choices = [(c.id, f"{c.course_name} ({c.course_id})") for c in Course.query.all()]
    form.semester_id.choices = [(s.id, f"{s.year} ({s.term})") for s in Semester.query.all()]
    if form.validate_on_submit():
        try:
            if StudentsCourses.query.filter_by(course_id=form.course_id.data).count() >= Course.query.get(form.course_id.data).capacity:
                flash("Course is out of capacity", "danger")
                return redirect(url_for("admin.add_enrollment"))
            
            enrollment = StudentsCourses(
                student_id=form.student_id.data,
                course_id=form.course_id.data,
                semester_id=form.semester_id.data,
                enrollment_date=form.enrollment_date.data,
                grade=form.grade.data
            )
            db.session.add(enrollment)
            
            student_semester = StudentSemester.query.filter_by(
                            student_id=form.student_id.data,
                            semester_id=form.semester_id.data
                            ).first()
            if not student_semester:
                student_semester = StudentSemester(
                student_id=form.student_id.data,
                semester_id=form.semester_id.data
                )
            db.session.add(student_semester)

            db.session.commit()
            logger.info(f"Enrollment created by admin for student {enrollment.student_id} in course {enrollment.course_id}.")
            flash("Enrollment created successfully", "success")
            return redirect(url_for("admin.home"))
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Admin failed to create enrollment. Student {form.student_id.data} is already enrolled in course {form.course_id.data}.")
            flash("That student is already enrolled in that course.", "danger")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during enrollment creation by admin: {e}")
            flash("A database error occurred. Please try again.", "danger")
    return render_template("admin/create_enrollment.html", form=form)

@admin_bp.route("/enrollment/<int:student_id>/<int:course_id>/<int:semester_id>/edit", methods=["POST", "GET"])
@login_required
@admin_required
def edit_enrollment(student_id, course_id, semester_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id, semester_id=semester_id).first_or_404()
    form = EnrollmentForm(obj=enrollment)
    form.student_id.choices = [(s.id, f"{s.first_name} {s.last_name}") for s in Student.query.all()]
    form.course_id.choices = [(c.id, f"{c.course_name} ({c.course_id})") for c in Course.query.all()]
    form.semester_id.choices = [(s.id, f"{s.year} ({s.term})") for s in Semester.query.all()]
    if form.validate_on_submit():
        try:
            enrollment.student_id = form.student_id.data
            enrollment.course_id = form.course_id.data
            enrollment.semester_id = form.semester_id.data
            enrollment.enrollment_date = form.enrollment_date.data
            enrollment.grade = form.grade.data
            db.session.commit()
            logger.info(f"Enrollment updated by admin for student {enrollment.student_id} in course {enrollment.course_id}.")
            flash("Enrollment updated!", "success")
            return redirect(url_for("admin.home"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during enrollment update by admin for student {enrollment.student_id} in course {enrollment.course_id}: {e}")
            flash("A database error occurred. Please try again.", "danger")
    
    return render_template("admin/edit_enrollment.html", enrollment=enrollment, form=form)

@admin_bp.route("/enrollment/<int:student_id>/<int:course_id>/<int:semester_id>/delete", methods=["POST", "GET"])
@login_required
@admin_required
def delete_enrollment(student_id, course_id, semester_id):
    enrollment = StudentsCourses.query.filter_by(student_id=student_id, course_id=course_id, semester_id=semester_id).first_or_404()
    if request.method == "POST":
        try:
            db.session.delete(enrollment)
            db.session.commit()
            logger.info(f"Enrollment deleted by admin for student {enrollment.student_id} in course {enrollment.course_id}.")
            flash("Enrollment deleted successfully!", "success")
            return redirect(url_for("admin.show_enrollments"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during enrollment deletion by admin for student {enrollment.student_id} in course {enrollment.course_id}: {e}")
            flash("A database error occurred. Please try again.", "danger")
            return redirect(url_for("admin.show_enrollments"))
    return render_template("admin/delete_enrollment.html", enrollment=enrollment)

@admin_bp.route("/toggle-enrollment", methods=["POST"])
@login_required
@admin_required
def toggle_enrollment():
    try:
        setting = Setting.query.first()
        setting.enrollment_open = not setting.enrollment_open
        db.session.commit()
        logger.info(f"Enrollment toggled to {'open' if setting.enrollment_open else 'closed'} by admin.")
        flash(f"Enrollment is now {'open' if setting.enrollment_open else 'closed'}.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while toggling enrollment: {e}")
        flash("A database error occurred. Please try again.", "danger")
    return redirect(url_for("admin.home"))

@admin_bp.route("/semesters")
@login_required
@admin_required
def semesters():
    try:
        all_semesters = Semester.query.order_by(Semester.year.desc(), Semester.start_date.desc()).all()
        logger.info("Admin successfully retrieved the list of semesters.")
        return render_template("admin/semesters.html", semesters=all_semesters)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching semesters: {e}")
        flash("A database error occurred while fetching the list of semesters. Please try again later.", "danger")
        return render_template("admin/semesters.html", semesters=[])


@admin_bp.route("/semesters/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_semester():
    form = SemesterForm()
    if form.validate_on_submit():
        try:
            new_semester = Semester(
                year=form.year.data,
                term=form.term.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data
            )
            db.session.add(new_semester)
            db.session.commit()
            logger.info(f"Admin created a new semester: {new_semester.year} {new_semester.term}")
            flash("Semester created successfully.", "success")
            return redirect(url_for("admin.semesters"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during semester creation: {e}")
            flash("A database error occurred. Could not create the semester.", "danger")
    return render_template("admin/create_semester.html", form=form, title="Create Semester")


@admin_bp.route("/semesters/edit/<int:semester_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_semester(semester_id):
    semester = Semester.query.get_or_404(semester_id)
    form = SemesterForm(obj=semester)
    if form.validate_on_submit():
        try:
            semester.year = form.year.data
            semester.term = form.term.data
            semester.start_date = form.start_date.data
            semester.end_date = form.end_date.data
            db.session.commit()
            logger.info(f"Admin updated semester {semester_id}.")
            flash("Semester updated successfully.", "success")
            return redirect(url_for("admin.semesters"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while updating semester {semester_id}: {e}")
            flash("A database error occurred. Could not update the semester.", "danger")
    return render_template("admin/edit_semester.html", form=form, semester=semester, title="Edit Semester")


@admin_bp.route("/semesters/delete/<int:semester_id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_semester(semester_id):
    semester = Semester.query.get_or_404(semester_id)
    if request.method == "POST":
        try:
            db.session.delete(semester)
            db.session.commit()
            logger.info(f"Admin deleted semester {semester_id}.")
            flash("Semester has been deleted.", "success")
            return redirect(url_for("admin.semesters"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while deleting semester {semester_id}: {e}")
            flash("A database error occurred. The semester could not be deleted.", "danger")
            return redirect(url_for("admin.semesters"))
    return render_template("admin/delete_semester.html", semester=semester)


@admin_bp.route("/posts")
def show_posts():
    try:
        posts = Post.query.all()
        logger.info("Admin retrieved all posts successfully.")
        return render_template("admin/posts.html", posts=posts)
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching posts: {e}")
        flash("A database error occurred while fetching the list of posts. Please try again later.", "danger")
        return render_template("admin/semesters.html", semesters=[])

@admin_bp.route("/posts/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
           post = Post(
               title=form.title.data,
               content=form.content.data,
               admin_id=current_user.id,
           )
           db.session.add(post)
           db.session.commit()
           flash("Post created successfully.", "success")
           logger.info(f"Admin {current_user.id} created a post with id {post.id}")
           return redirect(url_for("admin.show_posts"))
       
        except SQLAlchemyError as e:
           db.session.rollback()
           logger.error(f"Database error during post creation: {e}")
           flash(f"Database error occured, Could not create post.", "danger")
    return render_template("admin/create_post.html", form=form, title="Create Post")           
    
    
@admin_bp.route("/posts/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            logger.info(f"Admin updated post {post_id}.")
            flash("post updated successfully.", "success")
            return redirect(url_for("admin.show_posts"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while updating post {post_id}: {e}")
            flash("A database error occurred. Could not update the post.", "danger")
    return render_template("admin/edit_post.html", form=form, post=post, title="Edit Post")


@admin_bp.route("/posts/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        try:
            db.session.delete(post)
            db.session.commit()
            logger.info(f"Admin deleted post {post_id}.")
            flash("Post has been deleted.", "success")
            return redirect(url_for("admin.show_posts"))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while deleting post {post_id}: {e}")
            flash("A database error occurred. The post could not be deleted.", "danger")
            return redirect(url_for("admin.show_posts"))
    return render_template("admin/delete_post.html", post=post)
