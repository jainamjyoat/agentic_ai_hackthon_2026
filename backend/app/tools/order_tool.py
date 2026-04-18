import json

def get_order(order_id: str):
    with open("app/data/orders.json") as f:
        orders = json.load(f)

    for o in orders:
        if o["order_id"] == order_id:
            return o

    return {"error": "Order not found"}