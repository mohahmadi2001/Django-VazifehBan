
# Use an official Python runtime as a parent image
FROM alpine:3.17

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE VazifeBan.settings

# Set working directory
WORKDIR .

# Install system dependencies
RUN apt-get update && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
