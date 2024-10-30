#!/bin/bash
set -e

mkdir /app/e_commerce/settings/static

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn e_commerce.wsgi:application --bind 0.0.0.0:${PORT:-8001} --workers 3
