from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI") (for sqlite DB)
    # for MySql
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://<{getenv('DB_USER')}>:<{getenv('DB_PASSWORD')}>@<{getenv('DB_HOST')}>:<{getenv('DB_PORT')}>/<{getenv('DB_NAME')}>"
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    
    MAIL_SERVER = getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = getenv('MAIL_USERNAME', 'your-email@example.com')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD', 'your-email-password')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER', '"Educational system"')