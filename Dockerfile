FROM python:3.10-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port for Render/Railway/etc
EXPOSE 8080

# Run the FastAPI app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "server:app"]
