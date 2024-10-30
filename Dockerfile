FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint first and make it executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application
COPY . /app/

# Specify the entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
