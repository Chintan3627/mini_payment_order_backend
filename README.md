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


# 6. Deployment (Gunicorn + Nginx)

## Gunicorn Service  
`config/gunicorn.service`:
```
[Unit]
Description=Gunicorn daemon
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/backend
ExecStart=/path/to/backend/venv/bin/gunicorn project.wsgi:application --bind unix:/run/gunicorn.sock --workers 3

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## Nginx Config  
`config/nginx.conf`:
```
server {
    listen 80;
    server_name your_domain_or_ip;

    location /static/ {
        alias /path/to/backend/static/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        include proxy_params;
    }
}
```

Enable:
```bash
sudo nginx -t
sudo systemctl restart nginx
```




