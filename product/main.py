from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from products import get_available_products, update_product_stock

app = FastAPI()

# ✅ Allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE...
    allow_headers=["*"],        # allow all headers
)

# Example endpoints
@app.get("/products")
def get_products(name: Optional[str] = None, category: Optional[str] = None):
    return get_available_products(name, category)

@app.put("/products/{product_id}/stock")
def update_stock(product_id: int, in_stock: bool):
    updated_product = update_product_stock(product_id, in_stock)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Stock updated successfully", "product": updated_product}

@app.get("/health")
def health_check():
    return {"status": "ok"}