# backend/Dockerfile
FROM python:3

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port
EXPOSE 5000

# Command to run the flask server
CMD ["python", "server.py"]
