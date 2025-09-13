# Import necessary modules from FastAPI, Pydantic, and requests
# Import typing for type annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

# Define the FastAPI application instance
app = FastAPI()
CART_SERVICE_URL = os.environ.get("CART_SERVICE_URL", "http://cart-service:8002")
# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# In-memory store for orders and mock inventory
orders: List[Dict] = []
mock_inventory = {
    1: 5,
    2: 10,
    3: 0  # Out of stock
}
class OrderRequest(BaseModel):
    username: str
    items: List[Dict] = [] 


# Endpoint to place an order
# Validates the cart, checks inventory, processes payment, and logs the order
@app.post("/order")
def place_order(request: OrderRequest):
    cart_items = get_cart_items(request.username)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    if not check_inventory(cart_items):
        log_order(request.username, "cancelled", reason="Out of stock")
        return {"status": "cancelled", "reason": "Out of stock"}

    if not mock_payment_check(request.username):
        log_order(request.username, "cancelled", reason="Payment failed")
        return {"status": "cancelled", "reason": "Payment failed"}

    deduct_inventory(cart_items)
    clear_cart(request.username)
    log_order(request.username, "confirmed")

    return {
        "status": "confirmed",
        "items": cart_items,
        "orders": [order for order in orders if order["user"] == request.username]
    }

# Endpoint to retrieve all orders for a specific user
@app.get("/order/{username}")
def get_user_orders(username: str):
    # Filter orders for the given username
    user_orders = [order for order in orders if order["user"] == username]
    if not user_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return {"orders": user_orders}

# ---------------------- Helpers ---------------------- #

# Helper function to retrieve cart items from the cart service
# Makes an HTTP GET request to the cart service
def get_cart_items(username: str):
    try:
        response = requests.get(f"{CART_SERVICE_URL}/cart/{username}", timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Cart service unavailable: {e}")

# Helper function to check inventory availability
# Ensures all items in the cart are in stock
def check_inventory(cart_items):
    for item in cart_items:
        if mock_inventory.get(item["product_id"], 0) < item["quantity"]:
            return False
    return True

# Helper function to deduct inventory
# Updates the mock inventory after an order is placed
def deduct_inventory(cart_items):
    for item in cart_items:
        mock_inventory[item["product_id"]] -= item["quantity"]

# Helper function to clear a user's cart
# Sends an HTTP DELETE request to the cart service
def clear_cart(username: str):
    try:
        requests.delete(f"{CART_SERVICE_URL}/cart/{username}/clear", timeout=3)
    except requests.RequestException as e:
        print(f"Warning: Failed to clear cart for {username}: {e}")

# Helper function to simulate a payment check
# Returns False for specific usernames to simulate payment failure
def mock_payment_check(username: str):
    return username != "fail"

# Helper function to log order details
# Logs the order status and reason (if any) to the console and in-memory store
def log_order(user: str, status: str, reason: str = None):
    msg = f"[ORDER] User: {user} -> Status: {status.upper()}"
    if reason:
        msg += f" | Reason: {reason}"
    print(msg)
    orders.append({"user": user, "status": status, "reason": reason})

@app.get("/health")
def health_check():
    return {"status": "ok"}