FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Select dependency set (defaults to minimal CPU-safe set)
ARG REQUIREMENTS_FILE=requirements-minimal.txt

# Copy requirements first for better caching
COPY requirements.txt requirements-minimal.txt ./

# Install Python dependencies with compatible versions
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

# Copy application files
COPY app.py .
COPY rc_xi_large_dataset.jsonl .

# Expose Gradio default port
EXPOSE 7860

# Set environment variables
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860
ENV CODETTE_FORCE_CPU=1
ENV CODETTE_ENABLE_OTEL=0

# Run the app
CMD ["python", "app.py"]
