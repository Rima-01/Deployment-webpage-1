# Use Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory inside the container
WORKDIR /app

# Copy only requirements to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8003

# Define environment variables for Django settings
ENV DJANGO_SETTINGS_MODULE=recommend_backend.settings
ENV ENV_FILE_LOCATION=/app/.env

# Run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8003"]
