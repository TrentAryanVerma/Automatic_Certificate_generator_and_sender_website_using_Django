# Evento

**Evento** is a Django-based web app for managing online and offline events such as tournaments and scrims. It features user authentication, profiles, event creation, and auto-generated certificates. The frontend is styled using Tailwind CSS for a responsive and modern UI.

## Features

- User registration and login
- Profile management
- Create and manage:
  - Tournaments
  - Scrims
  - General events
- Event dashboard (upcoming, ongoing, past)
- Certificate generation (PDF)
- Tailwind CSS-powered responsive design
- Admin panel for managing users and events

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Tailwind CSS
- **Database**: SQLite (default)
- **Others**: Pillow, WeasyPrint / ReportLab (for PDFs)

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git
- Virtualenv (recommended)

### Installation

```bash
git clone https://github.com/your-username/evento.git
cd evento

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Tailwind CSS Setup

If you're modifying styles, ensure django-tailwind is set up in the project.

Usage

Visit http://localhost:8000 to use the app.

Log in or register to create/join events.

Admin panel at /admin/ for superusers.


Folder Structure

evento/
├── evento/           # Project settings
├── events/           # Event and tournament logic
├── users/            # User registration and profiles
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── media/            # Uploaded files and certificates
└── requirements.txt

Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

License

This project is licensed under the MIT License.
