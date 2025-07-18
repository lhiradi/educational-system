import pytest
from src import create_app
from src.extensions import db
from src.models.admin import Admin
from src.models.teacher import Teacher
from src.models.student import Student
from src.models.course import Course
from src.models.semester import Semester
from src.models.students_courses import StudentsCourses
from datetime import datetime, timedelta

@pytest.fixture(scope='function')
def app():
    """Create a new Flask app instance for each test, using an in-memory SQLite DB."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SERVER_NAME": "localhost",
        "SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def init_database(app):
    """Populate the test DB with initial data."""
    with app.app_context():
        # Admin
        admin = Admin(
            first_name="Admin",
            last_name="Admini",
            admin_id="admin123",
            email="admin@gmail.com",
            national_id="1111111111",
            date_of_birth=datetime(2000, 2, 1)
        )
        admin.set_password("password")
        db.session.add(admin)

        # Teacher
        teacher = Teacher(
            first_name="John",
            last_name="Doe",
            teacher_id="teacher12",
            email="teacher@gmail.com",
            national_id="2222222222",
            date_of_birth=datetime(1990, 2, 1)
        )
        teacher.set_password("password")
        db.session.add(teacher)

        # Student
        student = Student(
            first_name="Jane",
            last_name="Doe",
            student_id="student1",
            email="student@gmail.com",
            date_of_birth=datetime(2005, 2, 1),
            national_id="3333333333"
        )
        student.set_password("password")
        db.session.add(student)

        # Semester
        start_date = datetime.now()
        end_date = start_date + timedelta(days=90)
        semester = Semester(
            start_date=start_date,
            end_date=end_date,
            year="2025",
            term="Fall"
        )
        db.session.add(semester)
        db.session.flush()

        # Course
        course = Course(
            course_name="Test",
            course_id="course1",
            course_unit=4,
            capacity=40,
            days="Sunday,Monday",
            teacher_id=teacher.id,
            start_date=start_date,
            end_date=end_date,
            start_time=datetime.strptime('09:00', '%H:%M').time(),
            end_time=datetime.strptime('11:00', '%H:%M').time()
        )
        db.session.add(course)
        db.session.flush()

        # Enrollment
        enrollment = StudentsCourses(
            student_id=student.id,
            course_id=course.id,
            semester_id=semester.id,
            enrollment_date=datetime.now(),
            grade=18
        )
        db.session.add(enrollment)

        db.session.commit()
        yield db

def login(client, user_id, password):
    """Helper function to log in a user."""
    return client.post('/login', data=dict(
        user_id=user_id,
        password=password
    ), follow_redirects=True)

def logout(client):
    """Helper function to log out a user."""
    return client.get('/logout', follow_redirects=True)