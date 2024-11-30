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

# Check if the database is ready before starting Gunicorn
echo "Waiting for database to be ready..."
until python manage.py dbshell -c "select 1;" > /dev/null 2>&1; do
    echo "Database is unavailable - sleeping"
    sleep 3
done
echo "Database is ready"

echo "Starting Gunicorn..."
exec gunicorn e_commerce.wsgi:application \
    --bind 0.0.0.0:${PORT:-8001} \
    --workers 3 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
