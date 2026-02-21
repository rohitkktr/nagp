FROM python:3.10-slim
WORKDIR /app

# Environment variables with defaults
# Order Service Configuration
ENV ORDER_PORT=8003
ENV ORDER_HOST=0.0.0.0
# Depends on Cart Service
ENV CART_SERVICE_URL=http://cart-service:8002

# These can be overridden at runtime with:
# docker run -e ORDER_PORT=8003 ...
# or in docker-compose.yml with the environment section

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]