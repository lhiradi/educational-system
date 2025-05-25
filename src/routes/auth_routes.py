from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from src.models.student import Student
from src.models.teacher import Teacher
from src.models.admin import Admin 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form["password"]
        user = (
            Student.query.filter_by(student_id=user_id).first() or
            Teacher.query.filter_by(teacher_id=user_id).first() or
            Admin.query.filter_by(admin_id=user_id).first()
        )
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))