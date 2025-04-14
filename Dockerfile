FROM pytorch/pytorch:2.2.2-cpu

# Disable GPU use (just in case)
ENV TRANSFORMERS_NO_GPU=true

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Launch app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
