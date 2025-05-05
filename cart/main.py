# Import necessary modules from FastAPI, Pydantic, and typing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Define the data model for a cart item
# Define the structure of a Cart Item
class CartItem(BaseModel):
    product_id: int
    quantity: int

# In-memory store for user carts
# In-memory store for carts
cart_db: Dict[str, List[CartItem]] = {}

# Define the FastAPI application instance
app = FastAPI()

# Endpoint to add items to a user's cart
# Initializes the cart if it doesn't exist and adds the item
@app.post("/cart/{username}/add")
async def add_to_cart(username: str, item: CartItem):
    cart_db.setdefault(username, []).append(item)
    return {"message": "Item added to cart", "cart": cart_db[username]}

# Endpoint to retrieve a user's cart
# Returns the cart if it exists, otherwise raises a 404 error
@app.get("/cart/{username}")
async def get_cart(username: str):
    if username not in cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart_db[username]

# Endpoint to clear a user's cart
# Empties the cart if it exists, otherwise raises a 404 error
@app.delete("/cart/{username}/clear")
async def clear_cart(username: str):
    if username not in cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_db[username] = []
    return {"message": f"{username}'s cart cleared"}
