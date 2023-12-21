# worker/Dockerfile

# Use an official Python 3.11 image on Alpine Linux as a parent image
FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the worker directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV NAME worker

# Run run_worker.py when the container launches
CMD ["python", "/app/run_worker.py"]

