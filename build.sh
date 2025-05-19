#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies"
pip install -r requirements.txt

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Running migrations"
python manage.py migrate

echo "Creating superuser if it doesn't exist"
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123');
    print('Superuser created');
else:
    print('Superuser already exists');
"

echo "Build completed successfully"