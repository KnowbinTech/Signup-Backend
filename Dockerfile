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
RUN mkdir /e_commerce/static/
RUN python manage.py collectstatic --noinput

# Expose the port that the app will run on
EXPOSE 8001

# Use Gunicorn to run the Django app
CMD gunicorn e_commerce.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers $((2 * $(nproc) + 1)) \
    --threads 3 \
    --timeout 60 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info
