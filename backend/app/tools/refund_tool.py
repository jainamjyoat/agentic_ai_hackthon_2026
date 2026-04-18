from .order_tool import get_order
from .product_tool import get_product

def check_refund_eligibility(order_id: str):
    order = get_order(order_id)

    if "error" in order:
        return order

    product = get_product(order["product_id"])

    if order["refund_status"] == "refunded":
        return {"status": "already_refunded"}

    return {
        "status": "eligible_check_needed",
        "order": order,
        "product": product
    }