# Educational System

This is a comprehensive web-based educational management system built with Flask. It provides a platform for managing students, teachers, courses, and enrollments, with distinct roles and functionalities for administrators, teachers, and students.

---

## Features

### Admin
- **Dashboard**: Central hub for all administrative tasks.
- **User Management**: Create, edit, and delete student and teacher accounts.
- **Course Management**: Create, edit, and delete courses, including details like course name, units, capacity, and schedule.
- **Enrollment Management**: Manually enroll or remove students from courses.
- **Semester Management**: Create, edit, and delete academic semesters.
- **Content Management**: Create, edit, and delete informational posts for all users.
- **System Settings**: Toggle enrollment status (open/closed) for the entire system.

### Teacher
- **Dashboard**: Access to teacher-specific functionalities.
- **Course Management**: View assigned courses and their details.
- **Student Management**: View enrolled students for each course, assign grades, and remove students from courses.

### Student
- **Dashboard**: Personalized dashboard with links to key student features.
- **Course Enrollment**: View available courses for the current semester and self-enroll.
- **Course Management**: View enrolled courses, assigned teachers, and grades.
- **Enrollment Finalization**: Finalize course selection for the semester.
- **Semester History**: View academic history, including past semesters and course details.

### General
- **Authentication**: Secure user login with password or One-Time Password (OTP) via email.
- **Role-Based Access Control**: Differentiated access levels and permissions for admins, teachers, and students.

---

## Project Structure

The project is organized into the following directories and files:

-   **`src/`**: Main source code directory.
    -   **`__init__.py`**: Initializes the Flask application and its extensions.
    -   **`configs/`**: Contains configuration files for the application.
    -   **`extensions/`**: Houses Flask extensions and custom decorators.
    -   **`forms/`**: Defines WTForms for handling user input and validation.
    -   **`models/`**: Contains SQLAlchemy database models.
    -   **`routes/`**: Manages application routes and views using Flask Blueprints.
    -   **`static/`**: Stores static assets like CSS and JavaScript files.
    -   **`templates/`**: Holds Jinja2 HTML templates for rendering views.
    -   **`utils/`**: Includes utility functions for tasks like email and logging.

---

## Technologies Used

-   **Backend**: Python, Flask
-   **Database**: Flask-SQLAlchemy (for any SQLAlchemy-compatible database)
-   **Authentication**: Flask-Login
--   **Forms**: Flask-WTF
-   **Frontend**: HTML, CSS (Bootstrap), JavaScript
-   **Environment Variables**: python-dotenv
-   **Email**: Flask-Mail

---

## Installation and Setup

1.  **Clone the repository**:
    ```bash
    git clone [https://your-repository-url.com/](https://your-repository-url.com/)
    cd educational-system
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the environment variables**:
    -   Create a `.env` file in the root directory.
    -   Add the following environment variables to the `.env` file, replacing the placeholder values with your actual configuration:
        ```env
        SECRET_KEY='your_strong_secret_key'
        SQLALCHEMY_DATABASE_URI='your_database_uri'  # e.g., 'sqlite:///project.db'
        SQLALCHEMY_TRACK_MODIFICATIONS=False

        # Email Configuration
        MAIL_SERVER='smtp.your-email-provider.com'
        MAIL_PORT=587
        MAIL_USE_TLS=True
        MAIL_USERNAME='your_email@example.com'
        MAIL_PASSWORD='your_email_password'
        MAIL_DEFAULT_SENDER='Your Name <your_email@example.com>'

        # Admin User Configuration
        ADMIN_ID='admin_user_id'
        ADMIN_EMAIL='admin@example.com'
        ADMIN_FIRST_NAME='Admin'
        ADMIN_LAST_NAME='User'
        ADMIN_NATIONAL_ID='1234567890'
        ADMIN_DOB='YYYY-MM-DD'
        ADMIN_PASSWORD='your_admin_password'
        ```

---

## Running the Application

To start the Flask development server, run the following command in the root directory:

```bash
flask run
```

The application will be accessible at `http://127.0.0.1:5000`.

---

## Usage

-   **Admin**: Log in with the admin credentials defined in your `.env` file to access the admin dashboard and manage the system.
-   **Teacher/Student**:
    -   An admin must first create teacher and student accounts.
    -   Once created, teachers and students can log in with their assigned credentials.
    -   Users can also opt to receive a One-Time Password (OTP) via email to log in.

---

This `README.md` file provides a comprehensive overview of the Educational System project, including its features, structure, setup instructions, and usage guidelines.
