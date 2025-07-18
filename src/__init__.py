from flask import Flask, session
from sqlalchemy.exc import SQLAlchemyError
import datetime
from dotenv import load_dotenv
from os import getenv
from src.configs.config import Config
from src.extensions import db,mail
from src.extensions import login_manager
from src.models.admin import Admin
from src.models.student import Student
from src.models.teacher import Teacher
from src.models.course import Course
from src.routes.main_routes import main_bp
from src.routes.auth_routes import auth_bp
from src.routes.admin_routes import admin_bp
from src.routes.teacher_routes import teacher_bp
from src.routes.student_routes import student_bp
from src.models.admin import Admin
from src.models.student import Student
from src.models.setting import Setting

load_dotenv()

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)
        
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(user_id):
        admin = Admin.query.get(int(user_id))
        if admin and session.get("user_type") == "admin":
            return admin
        teacher = Teacher.query.get(int(user_id))
        if teacher and session.get("user_type") == "teacher":
            return teacher
        
        return Student.query.get(int(user_id))
    
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

def setup_database(app, logger):
    with app.app_context():
        try:
            logger.info("Initializing DB...")
            db.create_all()
            logger.info("Database tables created or already exist.")
            
            if not Setting.query.first():
                logger.info("No settings found. Seeding initial settings.")
                db.session.add(Setting(enrollment_open=False))
                db.session.commit()
                logger.info("Initial settings seeded successfully.")
            if not Admin.query.filter_by(admin_id=getenv("ADMIN_ID")).first():
                logger.info(f"Admin user {getenv("ADMIN_ID")} not found, creating new admin.")
                admin = Admin()
                admin.admin_id = getenv("ADMIN_ID")
                admin.email = getenv("ADMIN_EMAIL")
                admin.first_name = getenv("ADMIN_FIRST_NAME")
                admin.last_name = getenv("ADMIN_LAST_NAME")
                admin.national_id = getenv("ADMIN_NATIONAL_ID") 
                admin.date_of_birth=getenv("ADMIN_DOB", datetime.date(2005, 2, 2))

                admin.set_password(getenv("ADMIN_PASSWORD"))
                db.session.add(admin)

                db.session.commit()
                logger.info("Admin user created.")
        except SQLAlchemyError as e:
            
            db.session.rollback()
            app.logger.error(f"DATABASE ERROR: An error occurred during database setup: {e}")
            raise
        except Exception as e:
            app.logger.error(f"UNEXPECTED ERROR: A non-database error occurred during setup: {e}")
            raise