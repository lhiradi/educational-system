from flask import url_for
from .conftest import login, logout

def test_login_logout(client, init_database):
    """
    GIVEN a user
    WHEN they log in and then log out
    THEN they should be redirected correctly and the session should be cleared
    """
    # Test login with correct credentials
    rv = login(client, 'admin123', 'password')
    assert rv.status_code == 200
    assert b'Welcome, Admin!' in rv.data

    # Test logout
    rv = logout(client)
    assert rv.status_code == 200
    assert b'Login' in rv.data

    # Test login with incorrect credentials
    rv = login(client, 'admin123', 'wrongpassword')
    assert rv.status_code == 200
    assert b'Invalid credentials' in rv.data

def test_admin_login(client, init_database):
    """Test admin login."""
    rv = login(client, 'admin123', 'password')
    assert b'Admin' in rv.data
    logout(client)

def test_teacher_login(client, init_database):
    """Test teacher login."""
    rv = login(client, 'teacher12', 'password')
    assert b'Teacher' in rv.data
    logout(client)

def test_student_login(client, init_database):
    """Test student login."""
    rv = login(client, 'student1', 'password')
    assert b'Student' in rv.data
    logout(client)

def test_unauthorized_access(client, init_database):
    """
    GIVEN a user who is not logged in
    WHEN they try to access a protected page
    THEN they should be redirected to the login page
    """
    # Try to access admin dashboard
    rv = client.get(url_for('admin.home'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Please log in to access this page.' in rv.data
    assert b'Login' in rv.data

    # Try to access teacher dashboard
    rv = client.get(url_for('teacher.teacher_home'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Please log in to access this page.' in rv.data
    assert b'Login' in rv.data

    # Try to access student dashboard
    rv = client.get(url_for('student.home'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Please log in to access this page.' in rv.data
    assert b'Login' in rv.data

def test_role_based_access(client, init_database):
    """
    GIVEN a logged-in user
    WHEN they try to access a page for a different role
    THEN they should be shown an unauthorized message
    """
    # Student tries to access admin page
    login(client, 'student1', 'password')
    rv = client.get(url_for('admin.home'), follow_redirects=True)
    assert rv.status_code == 403 
    logout(client)

    # Teacher tries to access admin page
    login(client, 'teacher12', 'password')
    rv = client.get(url_for('admin.home'), follow_redirects=True)
    assert rv.status_code == 403 
    logout(client)
