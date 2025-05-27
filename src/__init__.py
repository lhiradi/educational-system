from flask import Flask
from src.configs.config import Config
from src.extensions import db
from src.extensions import login_manager
from src.models.admin import Admin
from src.models.student import Student
from src.models.teacher import Teacher
from src.models.course import Course
from src.routes.main_routes import main_bp
from src.routes.auth_routes import auth_bp
from src.routes.admin_routes import admin_bp
from src.models.admin import Admin
from src.models.student import Student

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(user_id):
        admin = Admin.query.get(int(user_id))
        if admin:
            return admin
        return Student.query.get(int(user_id))
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app