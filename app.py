from sqlalchemy import true
from src import create_app
from src.extensions import db
from os import getenv
from dotenv import load_dotenv
from src.models.student import Student
from src.models.admin import Admin
from src.models.teacher import Teacher
from src.models.course import Course
from src.models.students_courses import StudentsCourses
import datetime
load_dotenv()

app = create_app()
app.secret_key = getenv("SECRET_KEY")

with app.app_context():
    db.create_all()
    # for test purpose
    admin = Admin()
    admin.admin_id = "admin002"
    admin.first_name="Sara"
    admin.last_name="Admini"
    admin.national_id="1q34567890" 
    admin.date_of_birth=datetime.date(2005, 2, 2)

    admin.set_password("admin")
    db.session.add(admin)

    db.session.commit()

 

if __name__ == "__main__":
    app.run(debug=True)