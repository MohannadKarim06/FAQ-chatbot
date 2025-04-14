FROM pytorch/pytorch:2.1.0-cpu

# Disable GPU usage in transformers (just in case)
ENV TRANSFORMERS_NO_GPU=true

WORKDIR /app

# Install system libraries (for sumy, nltk, etc.)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install remaining Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
