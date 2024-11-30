#!/bin/bash
set -e

# Create the static directory if it doesn't exist
if [ ! -d "/app/e_commerce/settings/static" ]; then
    echo "Creating static directory..."
    mkdir -p /app/e_commerce/settings/static
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --noinput



echo "Starting Gunicorn..."
exec gunicorn e_commerce.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 4 \
    --threads 3 \
    --access-logfile - \
    --error-logfile -
