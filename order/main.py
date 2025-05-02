from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# In-memory store for orders and mock inventory
orders = []
mock_inventory = {
    1: 5,
    2: 10,
    3: 0  # Out of stock
}

class OrderRequest(BaseModel):
    username: str

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

    return {"status": "confirmed", "items": cart_items}


# ---------------------- Helpers ---------------------- #

def get_cart_items(username: str):
    try:
        response = requests.get(f"http://cart-service:8002/cart/{username}", timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Cart service unavailable")

def check_inventory(cart_items):
    for item in cart_items:
        if mock_inventory.get(item["product_id"], 0) < item["quantity"]:
            return False
    return True

def deduct_inventory(cart_items):
    for item in cart_items:
        mock_inventory[item["product_id"]] -= item["quantity"]

def clear_cart(username: str):
    try:
        requests.delete(f"http://cart-service:8002/cart/{username}/clear", timeout=3)
    except requests.RequestException:
        print(f"Warning: Failed to clear cart for {username}")

def mock_payment_check(username: str):
    return username != "fail"

def log_order(user: str, status: str, reason: str = None):
    msg = f"[ORDER] User: {user} → Status: {status.upper()}"
    if reason:
        msg += f" | Reason: {reason}"
    print(msg)
    orders.append({"user": user, "status": status, "reason": reason})
