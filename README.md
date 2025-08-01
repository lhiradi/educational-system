# Educational System

This is a comprehensive web-based educational management system built with Flask. It provides a platform for managing students, teachers, courses, and enrollments, with distinct roles and functionalities for administrators, teachers, and students.

---

## Features

### Admin

- **Dashboard**: Central hub for all administrative tasks.
- **User Management**: Create, edit, and delete student and teacher accounts.
- **Course Management**: Create, edit, and delete courses, assign teachers.
- **Semester Management**: Define and manage academic semesters.
- **Enrollment Management**: Oversee student course enrollments.
- **System Posts**: Create and manage system-wide announcements.
- **View All Data**: Access lists of all students, teachers, courses, and semesters.

### Teacher

- **Dashboard**: Overview of assigned courses and quick links.
- **Course Management**: View courses assigned for the current semester.
- **Student Management**: View enrolled students per course and assign/update grades.
- **Semester History**: View history of semesters in which they have taught courses.

### Student

- **Dashboard**: Personalized overview of academic status.
- **Course Management**: View enrolled courses, assigned teachers, and grades.
- **Course Enrollment**: Enroll in available courses for the current semester (while enrollment is open).
- **Enrollment Finalization**: Finalize course selection for the semester (once ready).
- **Semester History**: View academic history, including past semesters and course details.

### General

- **Authentication**: Secure user login with password or One-Time Password (OTP) via email.
- **Role-Based Access Control**: Differentiated access levels and permissions for admins, teachers, and students.
- **Responsive Design**: User interface adapts to different screen sizes (Bootstrap 5).

---

## Project Structure

The project is organized into the following directories and files:

- **`src/`**: Main source code directory.
  - **`__init__.py`**: Initializes the Flask application and its extensions.
  - **`configs/`**: Contains configuration files for the application.
  - **`extensions/`**: Houses Flask extensions (SQLAlchemy, LoginManager, Mail) and custom decorators.
  - **`routes/`**: Contains the route definitions for different user roles (admin, auth, student, teacher).
  - **`models/`**: Defines the SQLAlchemy database models (e.g., User, Admin, Teacher, Student, Course, Semester, StudentsCourses, Post, StudentSemester, Setting).
  - **`forms/`**: Contains WTForms form definitions for data validation and rendering.
  - **`templates/`**: Holds the Jinja2 HTML templates, organized by user role and shared components (macros, base).
  - **`static/`**: Stores static assets like CSS, JavaScript, and images.
  - **`utils/`**: Includes utility modules for email sending and custom logging.
- **`tests/`**: Contains pytest test cases for the application.
- **`app.py`**: The main application entry point.
- **`requirements.txt`**: Lists the Python dependencies required to run the application.
- **`dockerfile`**: Provides instructions for building a Docker image for the application.
- **`.env`**: (Not included in repo) File for storing environment variables (secret keys, database URI, email config).
- **`README.md`**: This file, providing an overview and setup instructions.
- **`LICENSE`**: The software license (MIT).

---

## Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/lhiradi/educational-system.git
    cd educational-system
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the environment variables**:
    - Create a `.env` file in the root directory.
    - Add the following environment variables to the `.env` file, replacing the placeholder values with your actual configuration:
      ```env
      SECRET_KEY='your_strong_secret_key'
      SQLALCHEMY_DATABASE_URI='your_database_uri' # e.g., 'sqlite:///project.db' or 'mysql+pymysql://user:password@host:port/db_name'
      SQLALCHEMY_TRACK_MODIFICATIONS=False

      # Email Configuration (for OTP)
      MAIL_SERVER='smtp.your-email-provider.com'
      MAIL_PORT=587
      MAIL_USE_TLS=True
      MAIL_USERNAME='your_email@example.com'
      MAIL_PASSWORD='your_email_password'
      MAIL_DEFAULT_SENDER='Your Name <your_email@example.com>'

      # Initial Admin User Configuration
      ADMIN_ID='admin_user_id'
      ADMIN_EMAIL='admin@example.com'
      ADMIN_FIRST_NAME='Admin'
      ADMIN_LAST_NAME='User'
      ADMIN_NATIONAL_ID='1234567890'
      ADMIN_DOB='YYYY-MM-DD' # Format: YYYY-MM-DD
      ADMIN_PASSWORD='your_admin_password' # Strong password for the initial admin
      ```

5.  **Initialize the database**:
    - The application is configured to create database tables automatically on the first run using `db.create_all()`.
    - Run the application:
      ```bash
      python app.py
      ```
    - This should create the database schema based on your models and the `SQLALCHEMY_DATABASE_URI` specified in `.env`. It will also attempt to create the initial admin user.

6.  **(Optional) Run Tests**:
    - Ensure the test database configuration (if different) is handled in `tests/conftest.py`.
    - Run the tests using pytest:
      ```bash
      pytest
      ```

---

## Usage Guidelines

1.  **Start the Application**:
    ```bash
    python app.py
    ```
    The application will typically be accessible at `http://localhost:5000` (or the port specified by your environment).

2.  **Accessing the System**:
    - **Admin**: Log in with the admin credentials defined in your `.env` file to access the admin dashboard and manage the system.
    - **Teacher/Student**:
      - An admin must first create teacher and student accounts via the admin panel.
      - Once created, teachers and students can log in with their assigned User ID and password.
      - Users can also opt to receive a One-Time Password (OTP) via email to log in.

---

## UML Diagram
<img src="docs/UML.png" style="width: 600px; height: 400px;" alt="UML Diagram">

## ER Diagram
<img src="docs/ER.png" style="width: 600px; height: 400px;" alt="ER Diagram">

---
## Switching to MySQL (from SQLite)

By default, the application uses SQLite. To use MySQL:

1.  **Install a MySQL driver** (e.g., PyMySQL):
    ```bash
    pip install PyMySQL
    ```
    Add `PyMySQL` to your `requirements.txt`.

2.  **Update the Database URI in `.env`**:
    Change the `SQLALCHEMY_DATABASE_URI` line:
    ```env
    # Example using PyMySQL
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://username:password@host:port/database_name'
    ```
    Replace `username`, `password`, `host`, `port`, and `database_name` with your MySQL details.

3.  **Ensure Database and User Exist**: Create the database and user in MySQL with appropriate permissions.

4.  **(Optional) Configure Engine Options**: Add connection pooling options in your app config (e.g., in `src/__init__.py` or a config file):
    ```python
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    ```

5.  **Recreate/Run Migrations**: Ensure tables are created in the new MySQL database.

---

This `README.md` file provides a comprehensive overview of the Educational System project, including its features, structure, setup instructions, and usage guidelines.
