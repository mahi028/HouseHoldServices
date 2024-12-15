echo "Activating VENV"
# source env/bin/activate
echo "VENV Actiavted"

echo "Stating celery workers"

celery -A app.celery_app worker -l info
