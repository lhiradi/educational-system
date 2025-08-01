from src.extensions import db
from src.models.base_model import BaseModel
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash

class Teacher(BaseModel, UserMixin):
    __tablename__ = "teachers"
    
    teacher_id = db.Column(db.String(13), nullable=False, unique=True)
    
    courses = db.relationship('Course', back_populates='teacher', cascade="all, delete-orphan")
    
    @property
    def user_type(self):
        return "teacher"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_otp_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        otp = ''.join(random.choices(string.digits, k=6))   
        return otp, s.dumps({'otp': otp, 'user_id': self.id})

    @staticmethod
    def verify_otp_login_token(token, submitted_otp):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=600)
            if data['otp'] == submitted_otp:
                return Teacher.query.get(data['user_id'])
        except Exception:
            return None
        return None