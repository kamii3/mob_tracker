Secure Mobile Tracking Web Application 📍🛡️

A professional, full-stack Python web application designed for real-time geolocation tracking with a strong focus on cybersecurity best practices. This project was developed as a university-level demonstration of integrating browser APIs with a secure Flask backend.

🚀 Features

Core Functionality

Manual Tracking: Users can update their location with a single click.

Auto-Tracking: Periodic background updates (every 60 seconds) using a toggle switch.

Interactive Maps: Uses Leaflet.js and OpenStreetMap for high-performance mapping.

Location History: Users can view a timestamped table of their past movements.

Admin Global View: Administrators can view all registered users and their last known locations on a single global map.

Security Features

Authentication: Secure registration and login system.

Password Security: Passwords are hashed using PBKDF2 with SHA256 (via Werkzeug).

CSRF Protection: Every state-changing request is protected against Cross-Site Request Forgery.

Role-Based Access Control (RBAC): Strict separation between standard Users and Administrators.

Secure Sessions: Cookies configured with HttpOnly and SameSite=Lax flags.

Activity Logging: All sensitive events (logins, registrations) are logged to activity.log for auditing.

🛠️ Tech Stack

Backend: Python 3.x, Flask Framework

Database: SQLite (SQLAlchemy ORM)

Frontend: Bootstrap 5, JavaScript (ES6), Leaflet.js

Auth: Flask-Login

Security: Flask-WTF (CSRF)

📂 Project Structure

mob_tracker/
│── app.py              # Main application logic & routes
│── models.py           # SQLAlchemy Database models (User, Location)
│── config.py           # Secure app configurations
│── requirements.txt    # Python dependencies
│── activity.log        # Security & event logs
│── static/             # CSS and frontend assets
│── templates/          # HTML files (Jinja2)
└── database.db         # SQLite database file


💻 Local Setup

Clone the repository

git clone https://github.com/kamii3/mob_tracker
cd mob_tracker


Create a Virtual Environment

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate


Install Dependencies

pip install -r requirements.txt


Run the App

python app.py


The app will be available at http://127.0.0.1:5000.

🔑 Test Credentials

Role

Email

Password

Admin

admin@tracker.com

admin123

User

Register via UI

Set your own

🛡️ Ethical & Legal Disclaimer

For Educational Use Only.
This application is designed for educational and demonstration purposes. Tracking individuals without their explicit informed consent is illegal in many jurisdictions and violates privacy laws (GDPR, CCPA, etc.).

By using this software, you agree:

To obtain permission before tracking anyone.

To use the software in compliance with local laws.

That the developers are not liable for any misuse of the tool.

📜 License

Distributed under the MIT License. See LICENSE for more information.
