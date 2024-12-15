echo "Activating VENV"
# source env/bin/activate
echo "VENV Actiavted"

echo "Stating selery beat"

celery -A app.celery_app beat -l info
