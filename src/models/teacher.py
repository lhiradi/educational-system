from src.extensions import db
from src.models.base_model import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Teacher(BaseModel, UserMixin):
    __tablename__ = "teachers"
    
    teacher_id = db.Column(db.String, nullable=False, unique=True)
    
    courses = db.relationship('Course', back_populates='teacher', cascade="all, delete-orphan")
    
    @property
    def user_type(self):
        return "teacher"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)