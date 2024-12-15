#!bin/bash

echo "Installing Dependencies..."
pip install -r requirements.txt
echo "Dependencies Installed"

echo "Initialising Database..."
python3 -c "
from app import app
from application import db
app.app_context().push()
db.create_all()

print('Adding Users')
from application.modals import *
from application.modules.hash import hashpw
db.session.add(User(user_name = 'admin', role = 1, email = 'admin@gmail.com', password = hashpw('admin'), name = 'admin', contact_number = 123))
db.session.add(User(user_name = 'pro', role = 2, email = 'pro@gmail.com', password = hashpw('pro'), name = 'pro', contact_number = 123))
db.session.add(User(user_name = 'pro2', role = 2, email = 'pro2@gmail.com', password = hashpw('pro2'), name = 'pro2', contact_number = 123))
db.session.add(User(user_name = 'pro3', role = 2, email = 'pro3@gmail.com', password = hashpw('pro3'), name = 'pro3', contact_number = 123))
db.session.add(User(user_name = 'pro4', role = 2, email = 'pro4@gmail.com', password = hashpw('pro4'), name = 'pro4', contact_number = 123))
db.session.add(User(user_name = 'cust', role = 3, email = 'cust@gmail.com', password = hashpw('cust'), name = 'cust', contact_number = 123))
db.session.add(User(user_name = 'cust2', role = 3, email = 'cust2@gmail.com', password = hashpw('cust2'), name = 'cust2', contact_number = 123))
db.session.commit()
print('Users added')


print('Adding Services')
db.session.add(Service(name='Plumber', desc='Get your Plumbing needs take a rest by booking Verified Professionals.', base_price=300, min_time=30))
db.session.add(Service(name='Electrician', desc='Need an electrician? Book one now .', base_price=300, min_time=30))
db.session.add(Service(name='House Help', desc='need Someone to take care of your daily chores? Get a Verified House Help.', base_price=300, min_time=30))
db.session.add(Service(name='Tv Technician', desc='Install/Repair Tv.', base_price=300, min_time=30))
db.session.commit()
print('Services Added')

print('Adding Professionals')
db.session.add(ServicePro(id = 2, desc='I am a pro plumber', serv_id = 1, experience = '5', service_area_pin_code = 201011, id_document_url='http://localhost:5000/static/upload/user.png'))
db.session.add(ServicePro(id = 3, desc='I am a pro plumber', serv_id = 1, experience = '5', service_area_pin_code = 201011, id_document_url='http://localhost:5000/static/upload/user.png'))
db.session.add(ServicePro(id = 4, desc='I am a pro Electrician', serv_id = 2, experience = '5', service_area_pin_code = 201011, id_document_url='http://localhost:5000/static/upload/user.png'))
db.session.add(ServicePro(id = 5, desc='House Help', serv_id = 3, experience = '5', service_area_pin_code = 201011, id_document_url='http://localhost:5000/static/upload/user.png'))
db.session.commit()
print('Professionals Added')

print('Database tables created successfully.')
exit()"
echo "Database Initialisation Complete"

echo "Initialising Migration Setup..."
flask db init
flask db migrate -m 'Initial migration.'
flask db upgrade
echo "Migration Setup Complete"

echo "Starting Application"
python3 app.py
