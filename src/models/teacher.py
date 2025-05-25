from src.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class Teacher(db.Model, UserMixin):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String, nullable=False, unique=True)
    national_id = db.Column(db.String(10), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    courses = db.relationship('Course', back_populates='teacher')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)