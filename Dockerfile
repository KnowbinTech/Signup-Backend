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
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the container
COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
