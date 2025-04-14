FROM python:3.10-slim

ENV TRANSFORMERS_NO_GPU=true

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements (torch last to control its size)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu
# NOTE: We're installing torch from PyTorch's CPU-only wheel repo!

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
