from src.extensions import db

class Setting(db.Model):
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True)
    enrollment_open = db.Column(db.Boolean, default=False)