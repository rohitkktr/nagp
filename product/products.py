products = [
    {
        "id": 1,
        "name": "Apple iPhone 14",
        "description": "Smartphone with A15 Bionic chip",
        "price": 999,
        "category": "electronics",
        "in_stock": True
    },
    {
        "id": 2,
        "name": "Samsung TV 55inch",
        "description": "Smart LED TV with 4K",
        "price": 650,
        "category": "electronics",
        "in_stock": True
    },
    {
        "id": 3,
        "name": "Nike Shoes",
        "description": "Running shoes",
        "price": 120,
        "category": "apparel",
        "in_stock": False
    }
]

def get_available_products(name: str = None, category: str = None):
    result = [p for p in products if p["in_stock"]]
    if name:
        result = [p for p in result if name.lower() in p["name"].lower()]
    if category:
        result = [p for p in result if category.lower() in p["category"].lower()]
    return result

def update_product_stock(product_id: int, in_stock: bool):
    for product in products:
        if product["id"] == product_id:
            product["in_stock"] = in_stock
            return product
    return None