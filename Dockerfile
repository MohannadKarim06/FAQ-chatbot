# Use Hugging Face base image with torch + transformers pre-installed
FROM huggingface/transformers-pytorch-gpu:4.40.1

# Disable GPU (Fly has no GPU)
ENV TRANSFORMERS_NO_GPU=true

# Create working directory
WORKDIR /app

# Install remaining lightweight dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy only necessary app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
