# CarePoint Hospital Management System

A Django-based hospital management website for displaying departments and doctors, booking appointments, managing user accounts, and suggesting relevant medical specialists from symptom descriptions.

## Features

- Responsive hospital website
- Department and doctor listings
- Doctor profile images
- Appointment booking form
- User registration, login, and logout
- Django administration interface
- Smart symptom-based doctor recommendations
- MCP server tools for departments, doctors, and appointment counts
- Synthetic clinic data generation

## Technology Stack

- Python 3.11+
- Django 5.2
- SQLite
- HTML and CSS
- Pillow
- FastMCP

## Project Structure

```text
hms/
├── home/                 # Main website application
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── recommendation.py
├── hms/                  # Django project configuration
├── media/                # Uploaded doctor images
├── db.sqlite3            # Development database
├── manage.py
├── mcp_server.py         # MCP server
├── seed_clinic_data.py   # Sample data generator
└── requirements.txt
```

## Installation

### 1. Clone the project

```bash
git clone <repository-url>
cd hospital_management\ system/hms
```

### 2. Create and activate a virtual environment

Windows:

```powershell
py -3.11 -m venv env
env\Scripts\activate
```

Linux or macOS:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

## Optional Sample Data

Populate the database with sample departments, doctors, and synthetic appointments:

```bash
python manage.py shell -c "exec(open('seed_clinic_data.py', encoding='utf-8').read())"
```

This creates fictional data only. Do not use generated patient records as real medical data.

## Main Routes

| Route | Description |
|---|---|
| `/` | Home page |
| `/about/` | About page |
| `/doctors/` | Doctor directory |
| `/department/` | Department directory |
| `/booking/` | Appointment booking |
| `/smart_recommendation/` | Symptom-based doctor finder |
| `/login/` | User login |
| `/signup/` | User registration |
| `/contact/` | Contact information |
| `/admin/` | Django administration |

## Smart Doctor Recommendation

Enter symptoms such as:

- Skin rash and itching
- Chest pain
- Headache or migraine
- Bone or joint pain
- Fever or cough
- Eye pain or blurred vision
- Ear pain or sore throat

The recommender matches symptom keywords to doctor specializations. It is a guidance feature and does not diagnose medical conditions. Seek urgent medical care for severe or emergency symptoms.

## MCP Server

Start the MCP server over standard input/output:

```bash
python mcp_server.py
```

Available tools:

- `list_departments`
- `list_doctors`
- `count_appointments`

## Running Tests

```bash
python manage.py test home
```

Check the Django project configuration:

```bash
python manage.py check
```

## Docker

Build and run with Docker:

```bash
docker build -t carepoint-hospital .
docker run --rm -p 8000:8000 carepoint-hospital
```

Open <http://localhost:8000/>.

## License

Add your preferred license here.
