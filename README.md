<<<<<<< HEAD
# ViRoute 🚍
 Description: ViRoute is a web app for easy bus bookings with
 real-time tracking. Users can book, pay, and track their rides, while
 operators manage routes and schedules on a single platform.

## Authors 👷
- [Khoi Do](https://github.com/khoidm2004) (Project Manager + Tester + Deploy)
- [Dung Nguyen](https://github.com/pingviini314159) (Backend Dev)
- [Thong Truong](https://github.com/truonghoangthong) (Backend Dev)
- [Thang Tran](https://github.com/tranthangok) (Designer + Frontend Dev)
- [Nhi Nguyen](https://github.com/nhingnguyen) (Designer + Frontend Dev)

## Tech stacks 💻

## [Demo▶️]
=======
# ViRoute

ViRoute is a web application built using Django and Django REST framework. It provides functionalities for route management, user authentication via GitHub, and more.

## Features

- User authentication via GitHub
- Route management using OpenRouteService API
- JWT authentication for REST API
- MySQL database integration

## Requirements

- Python 3.x
- Django 5.1.2
- MySQL

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/khoidm2004/ViRoute
    git checkout -b Backend # Switch to the Backend branch
    cd viroute
    ```
2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the MySQL database:

    ```sql
    CREATE DATABASE viroute;
    CREATE USER 'root'@'localhost' IDENTIFIED BY 'your_password';
    GRANT ALL PRIVILEGES ON viroute.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
    USE viroute;
    ```

5. Apply the migrations:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Configuration

Update the `viroute/settings.py` file with your MySQL database credentials:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'viroute',
        'USER': 'root',
        'PASSWORD': 'your_password', # your_password means your password ^_^! 
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

## For changing database table variables

1. Delete the migrations folder in the app folder

2. Delete the database

    ```sql
    DROP DATABASE viroute;
    ```

3. Make migrations

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Apply data
    
    ```python
    python run fake_data.py
    ```
>>>>>>> 592a5eefc14a164ce25a6a058cb521ba155512e2
