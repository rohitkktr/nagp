FROM python:3.10-slim
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck
# HEALTHCHECK --interval=30s --timeout=10s --retries=3   CMD curl -f http://localhost:8000/health || exit 1
