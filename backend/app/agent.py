import json
import re
from app.llm import generate
from app.tools.tool_registry import TOOLS

# 🧠 Memory
chat_memory = {}


def clean_llm_output(text: str):
    text = text.strip()

    if "```" in text:
        text = text.replace("```json", "").replace("```", "").strip()

    return text


# 🔥 Extract order_id manually (IMPORTANT)
def extract_order_id(text: str):
    match = re.search(r"ORD-\d+", text)
    return match.group(0) if match else None


def run_agent(user_input: str, session_id: str = "default", external_data=None):
    try:
        # 🧠 Load memory
        history = chat_memory.get(session_id, [])
        history_text = "\n".join(history)

        # 🔥 Inject uploaded JSON
        data_context = ""
        if external_data:
            data_context = json.dumps(external_data, indent=2)

        # 🔥 STEP 0 — FORCE TOOL CALL (CRITICAL FIX)
        order_id = extract_order_id(user_input)

        if order_id:
            action = "check_refund_eligibility"
            parameters = {"order_id": order_id}
        else:
            # 🔹 STEP 1 — LLM decides
            prompt = f"""
You are an AI support agent.

You MUST use tools when required.

Available tools:
- check_refund_eligibility(order_id)
- escalate_ticket(reason)

Rules:
- If order_id is present → ALWAYS call check_refund_eligibility
- NEVER say you don't have access
- NEVER refuse

External Data:
{data_context}

Conversation history:
{history_text}

User: {user_input}

Respond ONLY in JSON:
{{
  "action": "tool_name OR final",
  "parameters": {{}},
  "response": ""
}}
"""

            raw_text = generate(prompt)
            text = clean_llm_output(raw_text)

            try:
                data = json.loads(text)
                action = data.get("action")
                parameters = data.get("parameters", {})
            except Exception:
                return {
                    "error": "Invalid LLM response",
                    "raw": text
                }

        # 🔹 STEP 2 — TOOL EXECUTION
        if action in TOOLS:
            tool_fn = TOOLS[action]

            try:
                # 🔥 Pass external_data into tool if needed
                tool_result = tool_fn(
                    **parameters,
                    external_data=external_data
                )
            except Exception as e:
                return {"error": f"Tool failed: {str(e)}"}

            # 🔥 STEP 3 — FINAL RESPONSE
            final_prompt = f"""
You are a customer support AI.

External Data:
{data_context}

User query:
{user_input}

Tool result:
{tool_result}

Write a helpful, human-friendly response.

Rules:
- DO NOT show raw JSON
- DO NOT say you lack access
- Use data provided
"""

            final_text = generate(final_prompt).strip()

        else:
            final_text = "I'm not sure how to help with that."

        # 🔥 STEP 4 — ESCALATION
        escalation_data = None

        if any(word in user_input.lower() for word in ["broken", "defect", "warranty", "replace"]):
            escalation_data = TOOLS["escalate_ticket"](
                "Complex issue requires human review"
            )

        # 🧠 SAVE MEMORY
        history.append(f"User: {user_input}")
        history.append(f"AI: {final_text}")
        chat_memory[session_id] = history[-10:]

        return {
            "response": final_text,
            "confidence": 0.9,
            "escalation": escalation_data
        }

    except Exception as e:
        return {"error": str(e)}