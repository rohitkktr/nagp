FROM python:3.10-slim
WORKDIR /app

# Environment variables with defaults
# Cart Service Configuration
ENV CART_PORT=8002
ENV CART_HOST=0.0.0.0

# These can be overridden at runtime with:
# docker run -e CART_PORT=8002 ...
# or in docker-compose.yml with the environment section

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]