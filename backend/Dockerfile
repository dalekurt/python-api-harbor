FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apk --no-cache add build-base libffi-dev openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base libffi-dev openssl-dev

# Expose port 8000 for FastAPI app
EXPOSE 8000

# Run uvicorn to start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
