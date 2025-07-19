
# Log Manager

Description

## Features

### Authentication & Accounts
- User login and registration
- Social login with Google and GitHub
- Account settings and profile management

### Organization Management
- Create, edit, and delete organizations
- Status control: active, inactive, archived
- Secure deletion confirmation
- Filtering support for quick access

### Project Management
- Create, edit, and delete projects
- Link projects to organizations
- Status control: active, inactive, archived
- Secure deletion confirmation

### Tech Highlights
- Django backend
- Bootstrap frontend
- HTMX for interactive UI components
- django-filter for filtering data
- widget-tweaks for improved form rendering
- social-django for social authentication

## Getting Started

```bash
git clone https://github.com/yourusername/log-manager.git
cd log-manager

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
