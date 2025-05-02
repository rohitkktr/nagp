from fastapi import FastAPI
from typing import List

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 800, "description": "Gaming Laptop", "available": True},
    {"id": 2, "name": "Phone", "category": "Electronics", "price": 500, "description": "Smartphone", "available": True},
    {"id": 3, "name": "Shoes", "category": "Fashion", "price": 100, "description": "Running Shoes", "available": False},
]

@app.get("/products")
def get_products(name: str = None, category: str = None):
    result = [p for p in products if p["available"]]
    if name:
        result = [p for p in result if name.lower() in p["name"].lower()]
    if category:
        result = [p for p in result if category.lower() in p["category"].lower()]
    return result