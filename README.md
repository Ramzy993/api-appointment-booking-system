# api-appointment-booking-system
This is an Appointment Booking System (ABS) Backend written with Python and Flask as a backend framework. 

**Technologies used**: 
- Docker
- Python
- Postgres
- SQLAlchemy


This project has a config file saved in this path. 
api-appointment-booking-system/src/common/conf/abs.conf.ini

- You can reconfigure this app by changing values inside this file.
- Also, you can override these values in test/prod env by changing env_overrides.json inside the same folder.
- generate_env.py is responsible for generating conf file in specified env.

**To run this project:**

<ol>
<li>git clone this project to you folder.</li>
<li>copy api-appointment-booking-system/project_files/docker-compose.yaml to your project root folder.</li>
<li>cd to your project folder.</li>
<li>write `docker-compose up --build` to build this project.</li>
<li>you can test this project apis using postman collection here api-appointment-booking-system/project_files/Appointment Management System.postman_collection.json.</li>
</ol>
