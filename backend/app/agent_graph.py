from langgraph.graph import StateGraph, END
from typing import TypedDict
import re

from .tools.order_tool import get_order
from .tools.refund_tool import check_refund_eligibility
from .tools.escalation_tool import escalate_ticket
from app.llm import call_llm


# 🔹 STATE
class AgentState(TypedDict):
    user_input: str
    order_id: str
    order: dict
    decision: str
    response: str


# 🔹 STEP 1: EXTRACT INFO
def extract_info(state: AgentState):
    text = state["user_input"]

    order_match = re.search(r"ORD-\d+", text)

    return {
        "order_id": order_match.group(0) if order_match else None
    }


# 🔹 STEP 2: FETCH ORDER
def fetch_order(state: AgentState):
    if not state.get("order_id"):
        return {"response": "Please provide your order ID."}

    order = get_order(state["order_id"])
    return {"order": order}


# 🔹 STEP 3: DECISION ENGINE
def decision_node(state: AgentState):
    order = state.get("order", {})

    if "error" in order:
        return {"decision": "invalid_order"}

    if order.get("refund_status") == "refunded":
        return {"decision": "already_refunded"}

    if order.get("status") == "delivered":
        return {"decision": "check_refund"}

    return {"decision": "unknown"}


# 🔹 STEP 4: REFUND CHECK
def refund_node(state: AgentState):
    result = check_refund_eligibility(state["order_id"])

    return {
        "response": f"Refund evaluation: {result}"
    }


# 🔹 STEP 5: ESCALATE
def escalate_node(state: AgentState):
    result = escalate_ticket("Manual review required")

    return {
        "response": f"Escalated: {result}"
    }


# 🔁 GRAPH BUILD
builder = StateGraph(AgentState)

builder.add_node("extract", extract_info)
builder.add_node("fetch_order", fetch_order)
builder.add_node("decision", decision_node)
builder.add_node("refund", refund_node)
builder.add_node("escalate", escalate_node)

builder.set_entry_point("extract")

builder.add_edge("extract", "fetch_order")
builder.add_edge("fetch_order", "decision")


# 🔀 ROUTING
def route_decision(state: AgentState):
    if state["decision"] == "check_refund":
        return "refund"
    elif state["decision"] == "invalid_order":
        return "escalate"
    else:
        return END


builder.add_conditional_edges("decision", route_decision)

builder.add_edge("refund", END)
builder.add_edge("escalate", END)

graph = builder.compile()


# 🚀 RUN AGENT
def run_agent(user_input: str):
    result = graph.invoke({
        "user_input": user_input
    })

    return result.get("response", "No response")