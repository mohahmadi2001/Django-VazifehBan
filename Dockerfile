
# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE VazifeBan.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
