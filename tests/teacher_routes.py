from flask import url_for
from .conftest import login, logout
from src.models.teacher import Teacher
from src.models.student import Student
from src.models.course import Course
from src.models.students_courses import StudentsCourses

def test_teacher_dashboard_access(client, init_database):
    """Test that only a teacher can access the teacher dashboard."""
    login(client, 'teacher12', 'password')
    rv = client.get(url_for('teacher.teacher_home'))
    assert rv.status_code == 200
    assert b'Teacher' in rv.data
    logout(client)

    login(client, 'student1', 'password')
    rv = client.get(url_for('teacher.teacher_home'))
    assert rv.status_code == 403 # Forbidden
    logout(client)

def test_teacher_view_courses(client, init_database):
    """
    GIVEN a logged-in teacher
    WHEN they view their courses
    THEN they should see the courses assigned to them
    """
    login(client, 'teacher12', 'password')
    rv = client.get(url_for('teacher.show_courses'))
    assert rv.status_code == 200
    assert b'Test' in rv.data
    assert b'course1' in rv.data
    logout(client)

def test_teacher_view_students_in_course(client, init_database):
    """
    GIVEN a logged-in teacher
    WHEN they view the students for one of their courses
    THEN they should see the enrolled students
    """
    login(client, 'teacher12', 'password')
    course = Course.query.filter_by(course_id='course1').first()
    rv = client.get(url_for('teacher.show_students', course_id=course.id))
    assert rv.status_code == 200
    assert b'Jane Doe' in rv.data # Student's name
    logout(client)

def test_teacher_edit_student_score(client, init_database):
    """
    GIVEN a logged-in teacher
    WHEN they edit a student's score for a course
    THEN the score should be updated in the database
    """
    login(client, 'teacher12', 'password')
    student = Student.query.filter_by(email='student@gmail.com').first()
    course = Course.query.filter_by(course_id='course1').first()
    enrollment = StudentsCourses.query.filter_by(student_id=student.id, course_id=course.id).first()
    assert int(enrollment.grade) == 18

    rv = client.post(url_for('teacher.edit_score', student_id=student.id, course_id=course.id), data={
        'grade': '95.5'
    }, follow_redirects=True)

    assert rv.status_code == 200
    assert b'Grade updated successfully' in rv.data

    updated_enrollment = StudentsCourses.query.filter_by(student_id=student.id, course_id=course.id).first()
    assert float(updated_enrollment.grade) == 95.5
    logout(client)