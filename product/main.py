# Import necessary modules from FastAPI and typing
from fastapi import FastAPI, HTTPException
from typing import List, Optional
# Import the function to retrieve available products
from products import get_available_products, update_product_stock

# Define the FastAPI application instance
app = FastAPI()

# Endpoint to retrieve products
# Filters products by name and category if query parameters are provided
@app.get("/products")
def get_products(name: Optional[str] = None, category: Optional[str] = None):
    return get_available_products(name, category)

@app.put("/products/{product_id}/stock")
def update_stock(product_id: int, in_stock: bool):
    updated_product = update_product_stock(product_id, in_stock)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Stock updated successfully", "product": updated_product}