Quicklic Backend
----------------
Quicklic provides a simple, yet efficient platform for doctors and 
patients to connect with each other. This platform contains restfull 
APIs for the client end applications.

Requirements
------------
Django Rest JWT is a Python Django based platform. 

- Python 3.4.3
- Django 1.11.4
- Postgres

Installation
------------
Following are the steps to install this platform.

- Get in the root directory of the project
- Create Virtual Environment
```sh
$ cd ..
$ virtualenv -p python3 quicklic_backend_venv
$ cd quicklic_backend
$ source ../quicklic_backend_venv/bin/activate
```
- Install Requirements
```sh
$ pip install -r requirements.txt
```
- Setting up the Database
```sh
$ cd quicklic_backend
$ pwd //It should display like this "/Users/(user)/quicklic_backend/quicklic_backend"
$ sudo vim local_settings.py
    //Add the code below and save the file
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'quicklic_backend',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    // Note: Settings are for POSTGRES SQL
$ cd .. 
$ python manage.py migrate 
```
