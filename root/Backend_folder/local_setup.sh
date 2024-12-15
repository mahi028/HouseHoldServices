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
exit()"
echo "Database Initialisation Complete"

echo "Initialising Migration Setup..."
flask db init
flask db migrate -m 'Initial migration.'
flask db upgrade
echo "Migration Setup Complete"

echo "Starting Application"
python3 app.py
