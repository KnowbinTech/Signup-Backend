FROM python:3.12.7

# Set the working directory
WORKDIR /

# Copy the requirements file
COPY requirements.txt .

# Install   
 dependencies
RUN pip install -r requirements.txt   


# Copy the project code
COPY . .

# Set environment variables (optional)
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Expose the port
EXPOSE 8000

# Command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
