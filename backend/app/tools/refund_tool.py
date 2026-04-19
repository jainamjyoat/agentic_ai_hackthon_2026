from datetime import datetime


def check_refund_eligibility(order_id: str, external_data=None):
    try:
        if not external_data:
            return {"error": "No data available"}

        orders = external_data.get("orders", [])
        products = external_data.get("products", [])

        # 🔍 Find order
        order = next((o for o in orders if o.get("order_id") == order_id), None)

        if not order:
            return {"status": "not eligible", "reason": "Order not found"}

        # 🔍 Find product
        product = next(
            (p for p in products if p.get("product_id") == order.get("product_id")),
            None
        )

        # 🚫 Not delivered
        if order.get("status") != "delivered":
            return {
                "status": "not eligible",
                "reason": "Order has not been delivered yet"
            }

        # 🚫 Product not returnable
        if product and product.get("returnable") is False:
            return {
                "status": "not eligible",
                "reason": "This product is not eligible for return"
            }

        # ⏳ Return window check
        if order.get("return_deadline"):
            try:
                deadline = datetime.strptime(order["return_deadline"], "%Y-%m-%d")
                if datetime.now() > deadline:
                    return {
                        "status": "not eligible",
                        "reason": "Return window has expired"
                    }
            except Exception:
                pass  # ignore format errors

        # ✅ Eligible
        return {
            "status": "eligible",
            "order": order,
            "product": product
        }

    except Exception as e:
        return {"error": str(e)}