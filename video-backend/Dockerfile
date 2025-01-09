# Step 1: Use an official Python base image
FROM python:3.9-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Prevent Python output from being buffered

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the backend code into the container
COPY . /app

# Step 5: Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 6: Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 7: Expose the port Django will run on
EXPOSE 8001

# Step 8: Define the command to run the backend server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
