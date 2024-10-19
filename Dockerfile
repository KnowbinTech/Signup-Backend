FROM python:3.12

#remove .env directory and create .env file
RUN rm -rf .env



# Set env Variables

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install  dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt   


# Copy the project code
COPY . /app/

# COllect static files
RUN python manage.py collectstatic --noinput


