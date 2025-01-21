# Dockerfile
FROM python:3.12-slim

# Update and clear cache
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=app.py

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
