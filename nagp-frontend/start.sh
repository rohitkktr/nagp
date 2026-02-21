#!/bin/sh

# Generate config.json from environment variables
echo "Generating config.json with environment variables..."
cat > /app/build/config.json << EOF
{
  "PUBLIC_PRODUCT_API": "${PUBLIC_PRODUCT_API:-http://localhost:8001}",
  "PUBLIC_CART_API": "${PUBLIC_CART_API:-http://localhost:8002}",
  "PUBLIC_ORDER_API": "${PUBLIC_ORDER_API:-http://localhost:8003}",
  "PUBLIC_AUTH_API": "${PUBLIC_AUTH_API:-http://localhost:8000}"
}
EOF

echo "Config.json generated:"
cat /app/build/config.json

# Ensure correct permissions
chmod 644 /app/build/config.json

# Start the server with verbose logging
echo "Starting HTTP server on port 3000..."
http-server build -p 3000 --gzip -c-1 -o
