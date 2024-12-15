# HouseHold Services
## Description
Plateforme where professionals can join and offer household services like electrician, plumbing etc and customers can book the service from the ease of their home.

## Technologies used
Backend: Flask, Vue.js, Celery, Redis, flask_jwt_extended, flask_bcrypt, flask_sqlalchemy, flask_wtf, Pinia, Vue-Router, Axios, Chart.js

# Project Setup

## Add environtment variables or add a .env file with following attributes
Add .env file in root/Backend_folder
```python
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_secret_key
WTF_SECRET_KEY=your_secret_key
CELERY_BROKER_URL = your_celery_broker_url_redis
CELERY_RESULT_BACKEND = your_celery_result_backend_url_redis
CACHE_REDIS_HOST = your_redis_host
CACHE_REDIS_PORT = your_redis_port
MAIL_SERVER = your_mail_server_host
MAIL_PORT = your_mail_server_port
MAIL_USERNAME = your_cred
MAIL_PASSWORD = your_cred
MAIL_DEFAULT_SENDER = your_cred
MAIL_USE_TLS = boolean
MAIL_USE_SSL = boolean
```

## Run following commands in your terminal for project setup 
### Backend initialisation

Crate a python local environment and activate it first or all the dependencies will be intsalled gloabaly.

For debian/linux
```sh
python3 -m venv env
source env/bin.activate
```
For windows
```sh
python -m venv env
./env/Scripts/activate.ps1
```

```sh
cd root/Backend_folder
sh local_setup.sh
```

### Frontend initialisation
Make sure you have installed npm, nodejs and vuejs on your system

For development
```sh
cd root/Frontend-folder
npm install
npm run dev
```
Create a build
```sh 
cd root/Frontend-folder
npm install
npm run build
```
Serve the build
```sh
will add command later
```

## Instrusctions for Celery initialisation
The application has some backend jobs that need celery to work and celery is currently available on linux only (check celery webpage for more info).

If you are working in windows environment either use WSL or don't run following commands. Some functionalities will be affected but most will work.

Also uncomment line 10-23 in root/Backend_folder/app.py to use scheduled task.
### Download WSL(Windows only)
```sh 
wsl --install
```

### celery worker initialisation
```sh
cd root/Backend_folder
sh worker.sh
```

### celery beat initialisation
```sh
cd root/Backend_folder
sh beat.sh
```

## Backend API endpoints
Note: Add prefix /api to access api endpoints.\
Authentication: "/get_csrf_token", "/login", "/logout"\
To register: "/register"\
Create/get Servicepro Account(post registration): "/create/service_pro", "/get/service_pro"\
Get/create customer account(post registration): "/create/customer", "/get/customer"\
Approve Service Pro (Admin only): "/professional/status/<int:id>/<string:action>"\
Service endpoints: "/create/service", "/update/service/<int:serv_id>",
"/delete/service/<int:serv_id>"\
Get all Services: "/services"\
Get Service by id: "/services/<int:serv_id>"\
Get all Professional Details: "/get/professionals"\
Get User Profile by id: "/profile/<int:id>"\
CompleteRequest: '/request/complete/<int:rqst_id>'\
Add Feedback: '/request/feedback/<int:rqst_id>'\
Get feedbacks on specific professionals: '/feedback/<int:serv_pro_id>'\
CreateServiceRequest: '/customer/service-requests', "/book_service/<int:serv_pro_id>",
'/request/<string:action>/<int:rqst_id>'\
ServiceReport(Admin only): "/create-report", "/get-report/<task_id>"\
FlagUser :"/flag-user/<int:id>"\
Statistics: "/dashboard/stats/<string:stat_type>"\
Currently stat_type options are only : [‘service’, ‘request’, service_request’]
