from sqlalchemy import true
from src import create_app, setup_database
from src.extensions import db
from os import getenv
from dotenv import load_dotenv
from src.models.student import Student
from src.models.admin import Admin
from src.models.teacher import Teacher
from src.models.course import Course
from src.models.students_courses import StudentsCourses
from src.models.setting import Setting
from src.utils.logger import Logger
import datetime
load_dotenv()

app = create_app()
app.secret_key = getenv("SECRET_KEY")
logger = Logger("app")

setup_database(app, logger)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except:
        logger.error("Failed to start app!")
        