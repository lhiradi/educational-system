from flask import flash, redirect, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"{current_user}.is_authenticated:", current_user.is_authenticated)
        print("current_user.is_admin:", getattr(current_user, "is_admin", None))
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            flash("Admin access required")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function