# worker/Dockerfile

# Use an official Python 3.11 image on Alpine Linux as a parent image
FROM python:3.11-alpine

# Set the working directory to /app (common convention in Docker containers)
WORKDIR /app

# Copy the shared directory contents into the container at /app/shared
COPY ./shared /app/shared

# Copy the worker directory contents into the container at /app/worker
COPY ./worker /app/worker

# Copy the run_worker.py script into the container at /app
COPY run_worker.py /app/

# Ensure the shared directory is recognized as a Python package
RUN touch /app/shared/__init__.py

# Install any needed packages specified in requirements.txt
# This assumes that the requirements.txt file is in the worker directory
RUN pip install --no-cache-dir -r /app/worker/requirements.txt

# Expose the port the worker will use
EXPOSE 7233

# Set the default environment variable for the task queue
ENV WORKER_TEMPORAL_TASK_QUEUE=api-queue

# Define environment variable
ENV NAME worker

# Run run_worker.py when the container launches
CMD ["python", "/app/run_worker.py"]
