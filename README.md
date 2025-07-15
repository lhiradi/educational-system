# Educational System

A comprehensive, multi-user educational management system built with Python and Flask. This application provides a robust platform for administrators, teachers, and students to manage courses, enrollments, and user data in an academic setting.

---

## ✨ Features

The application is designed with three distinct user roles, each with a specific set of permissions and functionalities.

### 👤 Admin
* **User Management:** Full CRUD (Create, Read, Update, Delete) capabilities for both student and teacher accounts.
* **Course Management:** Full CRUD for courses, including assigning teachers, setting class capacity, and defining schedules.
* **Enrollment Oversight:** Manually enroll or unenroll students from courses and view/edit all enrollment records.
* **System Control:** Open or close the global enrollment period for all students with a single click.

### 👩‍🏫 Teacher
* **Dashboard:** A personalized view of all assigned courses.
* **Student Rosters:** Access lists of students enrolled in each course.
* **Grade Management:** Easily assign, view, and update grades for individual students.
* **Course Administration:** Remove students from an assigned course.

### 🧑‍🎓 Student
* **Course Enrollment:** Browse and enroll in available courses. The system automatically prevents time conflicts and manages course capacity.
* **Personal Dashboard:** View enrolled courses, assigned teachers, schedules, and current grades.
* **Unit Validation:** The system enforces academic rules, ensuring students enroll in a valid number of units (between 14 and 24).
* **Finalize Enrollment:** A feature to lock in course selections for the academic term.

### 🔐 Authentication
* **Secure Role-Based Login:** Standard login using a User ID and password.
* **OTP Login:** A convenient and secure password-less login option using a One-Time Password (OTP) sent to the user's registered email.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database ORM:** Flask-SQLAlchemy
* **Forms & Validation:** Flask-WTF
* **Authentication:** Flask-Login
* **Email Notifications:** Flask-Mail
* **Frontend Templating:** Jinja2
* **Styling & Scripting:** HTML, CSS, JavaScript
* **Environment Configuration:** python-dotenv

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.10+
* A virtual environment tool like `venv` (recommended).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/lhiradi/educational-system.git](https://github.com/lhiradi/educational-system.git)
    cd educational-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a file named `.env` in the project's root directory. Copy and paste the following content into it, replacing the placeholder values with your actual configuration.

    ```env
    # Flask App Secret Key (change this to a random string)
    SECRET_KEY='a_very_secret_and_secure_key'

    # Database Configuration (example uses SQLite)
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    # Default Admin User (created automatically on first run)
    ADMIN_ID='admin1'
    ADMIN_PASSWORD='securepassword123'
    ADMIN_EMAIL='admin@example.com'
    ADMIN_FIRST_NAME='Admin'
    ADMIN_LAST_NAME='User'
    ADMIN_NATIONAL_ID='1234567890'
    ADMIN_DOB='2000-01-01'

    # Email Server for OTP (example for Gmail)
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='your-email@gmail.com'
    MAIL_PASSWORD='your-gmail-app-password'
    MAIL_DEFAULT_SENDER='"Educational System" <your-email@gmail.com>'
    ```
    > **Note:** For Gmail, you will need to generate an **App Password** from your Google Account security settings to use for `MAIL_PASSWORD`.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will start on `http://127.0.0.1:5000`. The database file (`site.db`) and the default admin user will be created automatically the first time you run the app.

---

## 📁 Project Structure

The project is organized into modules for clarity and scalability, following standard Flask application design patterns.


educational-system/
│
├── app.py                # Main application entry point
├── requirements.txt      # List of Python dependencies
├── .env                  # Environment variables (you create this)
├── src/                  # Main source code
│   ├── init.py         # Application factory, blueprint registration
│   ├── configs/            # App configuration classes
│   ├── extensions/         # Flask extension instances (db, login_manager)
│   ├── forms/              # WTForms classes for data validation
│   ├── models/             # SQLAlchemy database models
│   ├── routes/             # Flask blueprints defining URL routes
│   ├── static/             # CSS, JavaScript, and image assets
│   ├── templates/          # Jinja2 HTML templates for all pages
│   └── utils/              # Helper functions (email, logging, etc.)
│
└── LICENSE               # Project license file


---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

&copy; 2025 hiradi
