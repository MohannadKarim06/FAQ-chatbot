FROM python:3.10-slim

WORKDIR /app

# Install only necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies early to leverage Docker caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
