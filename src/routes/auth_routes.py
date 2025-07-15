from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user
from src.utils.email import send_login_otp_email
from src.models.student import Student
from src.models.teacher import Teacher
from src.models.admin import Admin 
from src.utils.logger import Logger
from src.forms.auth_form import LoginForm, IDForm, OTPLoginForm

logger = Logger("auth")
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        user = (
            Student.query.filter_by(student_id=user_id).first() or
            Teacher.query.filter_by(teacher_id=user_id).first() or
            Admin.query.filter_by(admin_id=user_id).first()
        )
        
        user_type = None
        if isinstance(user, Admin):
            user_type = "admin"
        elif isinstance(user, Teacher):
            user_type = "teacher"
        else: 
            user_type = "student"
        
        
        if user and user.check_password(password):
            session["user_type"] = user_type
            login_user(user)
            logger.info(f"{user_id} logged in.")
            return redirect(url_for('main.index'))
        else:
            logger.warning(f"Failed login attempt from {user_id}")
            flash('Invalid credentials')
    return render_template('login.html', form=form)

@auth_bp.route('/login/otp', methods=["POST", "GET"] )
def request_otp_login():
    form = IDForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user = Student.query.filter_by(student_id=user_id).first() or Teacher.query.filter_by(teacher_id=user_id).first()

        if user:
            otp, token = user.get_otp_token()
            send_login_otp_email(user, otp)
            flash('An OTP has been sent to your registered email address.', 'info')
            return redirect(url_for('auth.verify_otp_login', token=token))
        else:
            flash("User ID not found!", "danger")
    return render_template('auth/request_otp_login.html', title='Login with OTP', form=form)


@auth_bp.route('/login/otp/verify/<token>', methods=['GET', 'POST'])
def verify_otp_login(token):
    form = OTPLoginForm()
    if form.validate_on_submit():
        submitted_otp = form.otp.data
        user = Student.verify_otp_login_token(token, submitted_otp) or Teacher.verify_otp_login_token(token, submitted_otp)

        if user:
            if isinstance(user, Student):
                session["user_type"] = "student"
            elif isinstance(user, Teacher):
                session["user_type"] = "teacher"
            login_user(user)
            flash('You have been logged in successfully!', 'success')
            if user.user_type == 'student':
                return redirect(url_for('student.home'))
            elif user.user_type == 'teacher':
                return redirect(url_for('teacher.home'))
        else:
            flash('Invalid or expired OTP.', 'danger')
            return redirect(url_for('auth.request_otp_login'))

    return render_template('auth/verify_otp_login.html', title='Enter OTP', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))