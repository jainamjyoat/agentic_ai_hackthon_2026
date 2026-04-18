def escalate_ticket(reason: str):
    return {
        "status": "escalated",
        "reason": reason,
        "priority": "high"
    }