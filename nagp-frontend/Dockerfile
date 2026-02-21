# Build stage
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:22-alpine

WORKDIR /app

# Install a simple HTTP server to serve the built frontend
RUN npm install -g http-server

# Copy built application from builder stage
COPY --from=builder /app/build ./build

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 3000

# Environment variables with defaults
# API endpoints for microservices
ENV PUBLIC_PRODUCT_API=http://localhost:8001
ENV PUBLIC_CART_API=http://localhost:8002
ENV PUBLIC_ORDER_API=http://localhost:8003
ENV PUBLIC_AUTH_API=http://localhost:8000

# These can be overridden at runtime with:
# docker run -e PUBLIC_PRODUCT_API=http://your-host:8001 ...
# or in docker-compose.yml with the environment section

# Start the application
CMD ["/app/start.sh"]
