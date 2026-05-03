# Use a slim version of the Python base image for a smaller footprint
FROM python:3.11-slim as builder

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (e.g., build-essential if needed for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a separate directory to facilitate multi-stage builds
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Final stage: build the production image
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . .

# Create a non-root user for security and switch to it
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Use uvicorn to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
