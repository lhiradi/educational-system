from src.extensions import db
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    #TODO: add unique 
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)