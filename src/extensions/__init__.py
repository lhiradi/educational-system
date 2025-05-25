from flask import flash, redirect, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

from flask_login import current_user
from flask import flash, redirect, url_for
from functools import wraps

db = SQLAlchemy()

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
            flash("Admin access required.")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function