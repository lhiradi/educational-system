from flask import url_for
from .conftest import login, logout
from src.models.teacher import Teacher
from src.models.student import Student
from src.models.course import Course
from src.models.semester import Semester
from src.models.students_courses import StudentsCourses
from src.models.student_semester import StudentSemester
from datetime import datetime, timedelta
from src.extensions import db

def login_admin(client):
    login(client, 'admin123', 'password')

def test_admin_dashboard_access(client, init_database):
    login_admin(client)
    rv = client.get(url_for('admin.home'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Admin' in rv.data
    logout(client)

    login(client, 'teacher12', 'password')
    rv = client.get(url_for('admin.home'), follow_redirects=True)
    assert rv.status_code == 403
    logout(client)

def test_admin_view_teachers(client, init_database):
    login_admin(client)
    rv = client.get(url_for('admin.show_teachers'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'All Teachers' in rv.data
    assert b'John' in rv.data
    logout(client)

def test_admin_create_teacher(client, init_database):
    login_admin(client)
    rv = client.post(url_for('admin.create_teacher'), data={
        'first_name': 'New', 'last_name': 'Teacher',
        'email': 'newteacher@test.com',
        'password': 'newpassword',
        'teacher_id': 'newteacher1',
        'national_id': '1234567890',
        'date_of_birth': '2000-01-01'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Manage Teachers' in rv.data
    assert Teacher.query.filter_by(email='newteacher@test.com').first() is not None
    logout(client)

def test_admin_edit_teacher(client, init_database):
    login_admin(client)
    teacher = Teacher.query.filter_by(email='teacher@gmail.com').first()
    rv = client.post(url_for('admin.edit_teacher', id=teacher.id), data={
        'first_name': 'Johnathan', 'last_name': 'Doeman',
        'email': 'teacher@gmail.com', 'phone_number': '1234567899'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Teacher updated successfully' in rv.data
    updated_teacher = Teacher.query.get(teacher.id)
    assert updated_teacher.first_name == 'Johnathan'
    assert updated_teacher.last_name == 'Doeman'
    logout(client)

def test_admin_delete_teacher(client, init_database):
    login_admin(client)
    teacher = Teacher.query.filter_by(email='teacher@gmail.com').first()
    rv = client.post(url_for('admin.delete_teacher', id=teacher.id), follow_redirects=True)
    assert rv.status_code == 200
    assert Teacher.query.get(teacher.id) is None
    logout(client)

def test_admin_view_students(client, init_database):
    login_admin(client)
    rv = client.get(url_for('admin.show_students'))
    assert rv.status_code == 200
    assert b'All Students' in rv.data
    assert b'Jane' in rv.data
    logout(client)

def test_admin_create_student(client, init_database):
    login_admin(client)
    rv = client.post(url_for('admin.create_student'), data={
        'first_name': 'New', 'last_name': 'Student',
        'email': 'newstudent@test.com', 'phone_number': '5544332211',
        'password': 'newpassword', 'confirm_password': 'newpassword',
        'student_id': 'newstudent1', 'date_of_birth': '2005-01-01', 'national_id': '0987654321'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Manage Students' in rv.data
    assert Student.query.filter_by(email='newstudent@test.com').first() is not None
    logout(client)

def test_admin_edit_student(client, init_database):
    login_admin(client)
    student = Student.query.filter_by(email='student@gmail.com').first()
    rv = client.post(url_for('admin.edit_student', id=student.id), data={
        'first_name': 'Janet', 'last_name': 'Doer',
        'email': 'student@gmail.com', 'phone_number': '0987654322'
    }, follow_redirects=True)
    assert rv.status_code == 200
    updated_student = Student.query.get(student.id)
    assert updated_student.first_name == 'Janet'
    logout(client)

def test_admin_delete_student(client, init_database):
    login_admin(client)
    student = Student.query.filter_by(email='student@gmail.com').first()
    rv = client.post(url_for('admin.delete_student', id=student.id), follow_redirects=True)
    assert rv.status_code == 200
    assert Student.query.get(student.id) is None
    logout(client)

def test_admin_view_courses(client, init_database):
    login_admin(client)
    rv = client.get(url_for('admin.show_courses'))
    assert rv.status_code == 200
    assert b'All Courses' in rv.data
    assert b'Test' in rv.data
    logout(client)

def test_admin_create_course(client, init_database):
    login_admin(client)
    teacher = Teacher.query.first()
    semester = Semester.query.first()
    rv = client.post(url_for('admin.create_course'), data={
        'course_name': 'Advanced Testing', 'course_id': 'TEST202',
        'course_unit': 3, 'teacher_id': teacher.id,
        'days': 'Tuesday,Thursday',
        'start_time': '11:00', 'end_time': '12:30', 'capacity': 30,
        'start_date': '2025-07-18', 'end_date':'2025-07-30'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert Course.query.filter_by(course_id='TEST202').first() is not None
    logout(client)

def test_admin_edit_course(client, init_database):
    login_admin(client)
    course = Course.query.filter_by(course_id='course1').first()
    rv = client.post(url_for('admin.edit_course', id=course.id), data={
        'course_name': 'Intro to Testing - Updated', 'course_id': 'TEST101-U',
        'teacher_id': course.teacher_id,
        'days': course.days,
        'start_time': course.start_time.strftime('%H:%M'),
        'end_time': course.end_time.strftime('%H:%M'),
        'course_unit': 4, 'capacity': 40
    }, follow_redirects=True)
    assert rv.status_code == 200
    updated_course = Course.query.get(course.id)
    assert updated_course.course_name == 'Intro to Testing - Updated'
    assert updated_course.course_id == 'TEST101-U'
    logout(client)

def test_admin_delete_course(client, init_database):
    login_admin(client)
    course = Course.query.filter_by(course_id='course1').first()
    rv = client.post(url_for('admin.delete_course', id=course.id), follow_redirects=True)
    assert rv.status_code == 200
    assert Course.query.get(course.id) is None
    logout(client)

def test_admin_view_semesters(client, init_database):
    login_admin(client)
    rv = client.get(url_for('admin.semesters'))
    assert rv.status_code == 200
    assert b'Manage Semesters' in rv.data
    assert b'Fall' in rv.data and b'2025' in rv.data
    logout(client)

def test_admin_create_semester(client, init_database):
    login_admin(client)
    start_date = (datetime.now() + timedelta(days=100)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=190)).strftime('%Y-%m-%d')
    rv = client.post(url_for('admin.create_semester'), data={
        'year': '2026', 'term': 'Spring', 'start_date': start_date, 'end_date': end_date
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Spring' in rv.data and b'2026' in rv.data
    assert Semester.query.filter_by(year='2026').first() is not None
    logout(client)

def test_admin_delete_semester(client, init_database):
    login_admin(client)
    semester = Semester.query.filter_by(year='2025', term='Fall').first()
    rv = client.post(url_for('admin.delete_semester', semester_id=semester.id), follow_redirects=True)
    assert rv.status_code == 200
    assert Semester.query.get(semester.id) is None
    logout(client)

def test_admin_view_enrollments(client, init_database):
    login_admin(client)
    rv = client.get(url_for('admin.show_enrollments'))
    assert rv.status_code == 200
    assert b'Enrollments' in rv.data
    assert b'Jane' in rv.data and b'Test' in rv.data
    logout(client)

def test_admin_create_enrollment(client, init_database):
    login_admin(client)
    semester = Semester.query.first()
    if not semester:
        semester = Semester(year=2025, term="Fall", start_date=datetime(2025, 9, 1), end_date=datetime(2025, 12, 15))
        db.session.add(semester)
        db.session.commit()
    student = Student(
        first_name='Enroll',
        last_name='Me',
        email='enrollme@test.com',
        student_id='enrollme1',
        national_id='1122334455',
        date_of_birth=datetime(2006, 5, 5)
    )
    student.set_password('p')
    db.session.add(student)
    db.session.commit()
    teacher = Teacher.query.first()
    assert teacher is not None, "Default teacher not found in test database."
    course = Course(
        course_name='Enrollment Course',
        course_id='ENRL101',
        teacher_id=teacher.id,
        days='Monday',
        start_time=datetime.strptime('01:00', '%H:%M').time(),
        end_time=datetime.strptime('02:00', '%H:%M').time(),
        start_date=datetime(2025, 7, 18),
        end_date=datetime(2025, 7, 30),
        course_unit=3,
        capacity=20
    )
    db.session.add(course)
    db.session.commit()
    rv = client.post(url_for('admin.add_enrollment'), data={
        'student_id': student.id,
        'course_id': course.id,
        'semester_id': semester.id,
        'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
        'grade': 18,
    }, follow_redirects=True)
    assert rv.status_code == 200

    enrollment = StudentsCourses.query.filter_by(
        student_id=student.id,
        course_id=course.id,
        semester_id=semester.id
    ).first()
    assert enrollment is not None


    student_semester = StudentSemester.query.filter_by(
        student_id=student.id,
        semester_id=semester.id
    ).first()
    assert student_semester is not None

    logout(client)

def test_admin_delete_enrollment(client, init_database):
    login_admin(client)
    enrollment = StudentsCourses.query.first()
    assert enrollment is not None, "Fixture did not create an enrollment to delete."
    student_id_to_delete = enrollment.student_id
    course_id_to_delete = enrollment.course_id
    semester_id_to_delete = enrollment.semester_id
    rv = client.post(url_for('admin.delete_enrollment',
                             student_id=student_id_to_delete,
                             course_id=course_id_to_delete,
                             semester_id=semester_id_to_delete),
                             follow_redirects=True)
    assert rv.status_code == 200
    deleted_enrollment = StudentsCourses.query.filter_by(
        student_id=student_id_to_delete,
        course_id=course_id_to_delete,
        semester_id=semester_id_to_delete
    ).first()
    assert deleted_enrollment is None

    student_semester = StudentSemester.query.filter_by(
        student_id=student_id_to_delete,
        semester_id=semester_id_to_delete
    ).first()
    assert student_semester is None

    logout(client)
