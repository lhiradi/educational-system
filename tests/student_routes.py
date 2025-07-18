from flask import url_for
from .conftest import login, logout
from src.models.student import Student
from src.models.course import Course
from src.models.semester import Semester
from src.models.students_courses import StudentsCourses
from src.extensions import db

def test_student_dashboard_access(client, init_database):
    """Test that only a student can access the student dashboard."""
    login(client, 'student1', 'password')
    rv = client.get(url_for('student.home'))
    assert rv.status_code == 200
    assert b'Student' in rv.data
    logout(client)

    login(client, 'teacher12', 'password')
    rv = client.get(url_for('student.home'))
    assert rv.status_code == 403 # Forbidden
    logout(client)

def test_student_view_current_courses(client, init_database):
    """
    GIVEN a logged-in student
    WHEN they view their courses for the current semester
    THEN they should see their enrolled courses
    """

    login(client, 'student1', 'password')
    rv = client.get(url_for('student.show_courses'))
    assert rv.status_code == 200
    assert b'My Courses' in rv.data
    assert b'Test' in rv.data
    assert b'course1' in rv.data
    logout(client)

def test_student_view_semester_history(client, init_database):
    """
    GIVEN a logged-in student
    WHEN they view their semester history
    THEN they should see a list of semesters they were enrolled in
    """
    login(client, 'student1', 'password')
    rv = client.get(url_for('student.semester_history'))
    assert rv.status_code == 200
    assert b'Semester History' in rv.data
    logout(client)

def test_student_view_semester_details(client, init_database):
    """
    GIVEN a logged-in student
    WHEN they view the details of a past semester
    THEN they should see the courses and grades for that semester
    """

    login(client, 'student1', 'password')
    semester = Semester.query.filter_by(year=2025).first()
    rv = client.get(url_for('student.semester_details', semester_id=semester.id))
    assert rv.status_code == 200
    assert b'Semester Details' in rv.data
    assert b'Test' in rv.data
    assert b'18' in rv.data # The score
    logout(client)
