# Mini Payment Order Backend – Installation Guide

Follow the steps below to set up the project on your local machine.

## 🚀 Installation Steps

### 1. Clone the Repository
git clone https://github.com/Chintan3627/mini_payment_order_backend.git
cd mini_payment_order_backend

### 2. Create Virtual Environment
python -m venv venv

### 3. Activate Virtual Environment
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Apply Migrations
python manage.py migrate

### 6. Create Superuser
python manage.py createsuperuser

### 7. Start the Development Server
python manage.py runserver

# Server URL
http://127.0.0.1:8000

## Notes
- Use Python 3.8 or higher.
- Activate the virtual environment before running Django commands.
- To update requirements.txt after installing new packages:
  pip freeze > requirements.txt



