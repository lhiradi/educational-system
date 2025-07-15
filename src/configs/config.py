from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    
    MAIL_SERVER = getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = getenv('MAIL_USERNAME', 'your-email@example.com')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD', 'your-email-password')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER', '"Educational system"')