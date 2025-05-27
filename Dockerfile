# Dockerfile
# Use a lightweight official Python image as a base
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories inside the container
# Ensure these match your actual structure
RUN mkdir -p App Trained_models metadata

# Copy your application code
COPY App/ App/

# Copy your trained models
COPY Trained_models/ Trained_models/

# Copy your metadata files
COPY metadata/ metadata/

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the application when the container starts
# Gunicorn is a production-ready WSGI server. It's better than Flask's built-in server.
# Install it first: pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "App.main:app"]