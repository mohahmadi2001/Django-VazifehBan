# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE VazifeBan.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
