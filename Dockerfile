# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
