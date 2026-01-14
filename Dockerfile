FROM python:3.11-slim

WORKDIR /app

# Install git and other dependencies
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/ChrisKoenig/techrob-action360-agent.git .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Run the API
CMD ["python", "run_api.py"]
