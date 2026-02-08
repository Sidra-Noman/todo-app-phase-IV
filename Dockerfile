# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /src

# Copy requirements file
COPY requirements.txt .

# Copy environment file
COPY .env .env


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Copy the application code
COPY app/ ./app/

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]