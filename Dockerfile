# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables for non-interactive installation
ENV PYTHONUNBUFFERED 1

# Install dependencies for PostgreSQL and SQLAlchemy
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && apk del gcc python3-dev musl-dev

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the necessary Python dependencies (SQLAlchemy, Flask-JWT-Extended)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow traffic to the app
EXPOSE 5000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

