import json

def get_product(product_id: str):
    with open("app/data/products.json") as f:
        products = json.load(f)

    for p in products:
        if p["product_id"] == product_id:
            return p

    return {"error": "Product not found"}