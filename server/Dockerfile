# server/Dockerfile

# Use an official Python 3.11 image on Alpine Linux as a parent image
FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the server directory contents into the container at /app
COPY . /app

# Copy the shared directory contents into the container at /app
COPY ../shared /app/shared

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME server

# Run the FastAPI app using Uvicorn when the container launches
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
