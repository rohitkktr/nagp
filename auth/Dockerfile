FROM python:3.10-slim
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Environment variables with defaults
# Auth Service Configuration
ENV AUTH_PORT=8000
ENV AUTH_HOST=0.0.0.0

# These can be overridden at runtime with:
# docker run -e AUTH_PORT=8000 ...
# or in docker-compose.yml with the environment section

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
