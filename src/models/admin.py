from src.extensions import db
from src.models.base_model import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(BaseModel, UserMixin):
    __tablename__ = "admins"
    
    admin_id = db.Column(db.String(13), nullable=False)
    
    @property
    def user_type(self):
        return "admin"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
