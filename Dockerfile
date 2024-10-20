# Use an official Python runtime as a parent image
FROM python:3.12.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port that the app will run on
EXPOSE 8001

# Use Gunicorn to run the Django app
CMD gunicorn e_commerce.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 2 \
    --threads 3 \
    --timeout 1000 \
    --max-requests 4000 \
    --max-requests-jitter 100 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info
