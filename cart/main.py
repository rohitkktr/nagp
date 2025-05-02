from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Define the structure of a Cart Item
class CartItem(BaseModel):
    product_id: int
    quantity: int

# In-memory store for carts
cart_db = {}

app = FastAPI()

# Endpoint to add items to the cart
@app.post("/cart/{username}/add")
async def add_to_cart(username: str, item: CartItem):
    # Initialize the user's cart if it doesn't exist
    if username not in cart_db:
        cart_db[username] = []

    # Add the item to the cart
    cart_db[username].append(item)
    return {"message": "Item added to cart", "cart": cart_db[username]}

# Endpoint to retrieve the cart of a user
@app.get("/cart/{username}")
async def get_cart(username: str):
    # Check if the user has a cart
    if username not in cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Return the cart for the user
    return cart_db[username]

# Endpoint to clear the cart of a user
@app.delete("/cart/{username}/clear")
async def clear_cart(username: str):
    # Check if the user has a cart
    if username not in cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Clear the user's cart
    cart_db[username] = []
    return {"message": f"{username}'s cart cleared"}
