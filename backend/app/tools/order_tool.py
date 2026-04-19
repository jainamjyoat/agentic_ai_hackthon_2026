import json

def get_order(order_id: str, external_data=None):
    try:
        # 🔥 FIX: correctly extract orders
        if external_data and "orders" in external_data:
            orders = external_data["orders"]
        else:
            with open("app/data/orders.json") as f:
                orders = json.load(f)

        # 🔍 Find order
        for o in orders:
            if o.get("order_id") == order_id:
                return o

        return {"error": f"Order {order_id} not found"}

    except Exception as e:
        return {"error": str(e)}