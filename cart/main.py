# Import necessary modules
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
import requests

# Define the data model for a cart item
class CartItem(BaseModel):
    product_id: int
    quantity: int

# In-memory store for user carts
cart_db: Dict[str, List[CartItem]] = {}

# Define the FastAPI application instance
app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # or ["http://localhost:5173"] for tighter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to add items to a user's cart
@app.post("/cart/{username}/add")
async def add_to_cart(username: str, item: CartItem):
    cart_db.setdefault(username, []).append(item)
    return {"message": "Item added to cart", "cart": cart_db[username]}

# Endpoint to retrieve a user's cart
@app.get("/cart/{username}")
async def get_cart(username: str):
    if username not in cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart_db[username]

# Endpoint to clear a user's cart
@app.delete("/cart/{username}/clear")
async def clear_cart(username: str):
    if username not in cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_db[username] = []
    return {"message": f"{username}'s cart cleared"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product-service:8001")

async def validate_product(product_id: int):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products?product_id={product_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Product not found")