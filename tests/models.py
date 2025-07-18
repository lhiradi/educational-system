from src.models.admin import Admin
from src.models.teacher import Teacher
from src.models.student import Student
from src.models.course import Course
from src.models.semester import Semester
from src.models.students_courses import StudentsCourses
from datetime import datetime, timedelta

def test_admin_model(init_database):
    """
    GIVEN a Admin model
    WHEN a new Admin is created
    THEN check the email and password hashing are defined correctly
    """
    admin = Admin.query.filter_by(email='admin@gmail.com').first()
    assert admin is not None
    assert admin.email == 'admin@gmail.com'
    assert admin.check_password('password')
    assert not admin.check_password('wrongpassword')

def test_teacher_model(init_database):
    """
    GIVEN a Teacher model
    WHEN a new Teacher is created
    THEN check the fields are defined correctly
    """
    teacher = Teacher.query.filter_by(email='teacher@gmail.com').first()
    assert teacher is not None
    assert teacher.first_name == 'John'
    assert teacher.last_name == 'Doe'
    assert teacher.check_password('password')

def test_student_model(init_database):
    """
    GIVEN a Student model
    WHEN a new Student is created
    THEN check the fields are defined correctly
    """
    student = Student.query.filter_by(email='student@gmail.com').first()
    assert student is not None
    assert student.first_name == 'Jane'
    assert student.last_name == 'Doe'
    assert student.check_password('password')

def test_semester_model(init_database):
    """
    GIVEN a Semester model
    WHEN a new Semester is created
    THEN check the fields are defined correctly
    """
    semester = Semester.query.filter_by(year="2025").first()
    assert semester is not None
    assert semester.start_date is not None
    assert semester.end_date is not None

def test_course_model(init_database):
    """
    GIVEN a Course model
    WHEN a new Course is created
    THEN check the fields and relationships are defined correctly
    """
    course = Course.query.filter_by(course_id="course1").first()
    assert course is not None
    assert course.course_name == 'Test'
    assert course.teacher.first_name == 'John'

def test_student_course_enrollment(init_database):
    """
    GIVEN Student and Course models
    WHEN a Student is enrolled in a Course
    THEN check the relationship is created correctly
    """
    student = Student.query.filter_by(email='student@gmail.com').first()
    course = Course.query.filter_by(course_id="course1").first()
    enrollment = StudentsCourses.query.filter_by(
        student_id=student.id,
        course_id=course.id
    ).first()

    assert enrollment is not None
    assert enrollment.student == student
    assert enrollment.course == course
    assert len(student.course_links) == 1
    assert len(course.student_links) == 1
    assert student.course_links[0].course.course_name == 'Test'
