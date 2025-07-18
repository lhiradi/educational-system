from flask import flash, redirect, url_for, abort
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from functools import wraps


db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def admin_required(f):
    from src.models.admin import Admin
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.")
            return redirect(url_for("auth.login"))
        admin = Admin.query.filter_by(national_id=current_user.national_id).first()
        if not admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    from src.models.teacher import Teacher
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.")
            return redirect(url_for("auth.login"))
        teacher = Teacher.query.filter_by(national_id=current_user.national_id).first()
        if not teacher:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    from src.models.student import Student
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not current_user.is_authenticated:
            flash("Please Log in to access this page.")
            return redirect(url_for("auth.login"))
        student = Student.query.filter_by(national_id=current_user.national_id).first()
        if not student:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function