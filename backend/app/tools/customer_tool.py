import json

def get_customer(email: str):
    with open("app/data/customers.json") as f:
        customers = json.load(f)

    for c in customers:
        if c["email"] == email:
            return c

    return {"error": "Customer not found"}