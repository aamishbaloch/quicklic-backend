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

Create a Super Admin to get things started. 
```sh
$ python manage.py createsuperuser
```
Access the Django Admin and login with the credentials. 

Seeds
-----
In order to populate mandatory data you need to run the management 
command that will auto populate items.
```sh
$ python manage.py seeds
```
This seeds will create a Super User and you can login to Django Admin 
Dashboard to perform needed actions. General details on the landing page
are also added with this script.

Setting up Error Reporting
--------------------------
To unable error reporting do the following, first add the following 
settings in your local_settings.py.
```sh
 EMAIL_USE_TLS = True
 EMAIL_HOST = 'smtp.gmail.com'
 EMAIL_HOST_USER = '{email}'
 EMAIL_HOST_PASSWORD = '{password}'
 EMAIL_PORT = 587
```
To add the recipients of these reports, you can add this in you settings.
```sh
ADMINS = (
  ('{name}', '{email}'),
)
```
You have to set **DEBUG=FALSE** in your settings to get these reports.

**Custom Error Reporting** can be configured. You can get the example of it 
in libs.error_reports.send_manually_error_email and 
libs.custom_exceptions.InvalidInputDataException. 


Timezone Setting
----------------
Don't forget to add your desired timezone setting in your local_settings.py.
```sh
TIME_ZONE = 'Asia/Karachi'
```
NOTE: Things won't work without adding this. 

In settings USE_TZ is set to be False. The reason of this is get the desired 
timezone from the DB as well so the comparison won't require any extra effort.


API Documentation
-----------------
We are using atlassian confluence for managing our documents. Here is 
the link for our API Documentation:
```sh
https://quicklic.atlassian.net/wiki/spaces/AD/pages
```

About the Landing Page
----------------------
We have an awesome landing page setup for this app.

### Contact Us
Contact Us form has been created on the landing page, through which 
customers or clients can reach us out. You can get the messages from 
the Admin Dashboard.

### Blog
We do have Blog posts on the Landing page as well, which can be entered 
by the Admin Dashboard. You simply need to add the author of the blog 
and ofcourse the content related to that.

### General Details
General details about the Application can be added dynamically from
the Admin Dashboard, that will be used throughout the landing page and
blog posts. Login to the dashboard to update the relative data.

**Note**: These details also be added to the dashboard when you run 
the seeds.


Quicklic Portal
---------------
Quicklic Portal is designed for doctors to access our features using our
web application. You can get the views in the portal app of this project.