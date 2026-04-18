import json
from .order_tool import get_order
from .customer_tool import get_customer
from .refund_tool import check_refund_eligibility
from .escalation_tool import escalate_ticket

TOOLS = {
    "get_order": get_order,
    "get_customer": get_customer,
    "check_refund_eligibility": check_refund_eligibility,
    "escalate_ticket": escalate_ticket,
}