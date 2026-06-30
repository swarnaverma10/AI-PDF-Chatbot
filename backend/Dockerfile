# ================================================================= #
# AI PDF Chatbot Backend - Hugging Face Spaces Dockerfile
# ================================================================= #

# Use a lightweight python base image
FROM python:3.11-slim as builder

# Set env vars to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies if any are needed (e.g., build-essential for compiling C deps)
# We use --no-install-recommends to keep the image slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies into a local directory (wheels)
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/user/.local/bin:$PATH

# Create a non-root user "user" with UID 1000 (required for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app

# Copy installed python dependencies from builder stage
COPY --from=builder --chown=user:user /root/.local /home/user/.local

# Copy application source code and knowledge base PDF
COPY --chown=user:user app/ ./app/
COPY --chown=user:user knowledge_base/ ./knowledge_base/

# Expose the default port for Hugging Face Spaces (7860)
EXPOSE 7860

# Start FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
