# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Install the build dependencies
RUN apt-get update && apt-get install -y build-essential

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port on which the Django development server will run
EXPOSE 8000

# Run the Django development server when the container starts
CMD python manage.py runserver 0.0.0.0:8000
