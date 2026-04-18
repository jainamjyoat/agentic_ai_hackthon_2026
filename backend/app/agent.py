import json
from app.llm import generate
from app.tools.tool_registry import TOOLS

# 🧠 In-memory session memory
chat_memory = {}


def clean_llm_output(text: str):
    """
    Remove markdown formatting if present
    """
    text = text.strip()

    if "```" in text:
        text = text.replace("```json", "").replace("```", "").strip()

    return text


def run_agent(user_input: str, session_id: str = "default"):
    try:
        # 🧠 Load memory
        history = chat_memory.get(session_id, [])
        history_text = "\n".join(history)

        # 🔹 STEP 1 — Ask LLM what to do
        prompt = f"""
Conversation history:
{history_text}

User: {user_input}
"""

        raw_text = generate(prompt)
        text = clean_llm_output(raw_text)

        try:
            data = json.loads(text)
        except Exception:
            return {
                "error": "Invalid LLM response",
                "raw": text
            }

        action = data.get("action")

        # 🔹 STEP 2 — Tool execution
        if action in TOOLS:
            tool_fn = TOOLS[action]

            try:
                tool_result = tool_fn(**data.get("parameters", {}))
            except Exception as e:
                return {"error": f"Tool execution failed: {str(e)}"}

            # 🔥 STEP 3 — Final response generation
            final_prompt = f"""
You are a customer support AI.

Conversation history:
{history_text}

User query:
{user_input}

Tool result:
{tool_result}

Now generate a FINAL response.

Rules:
- Do NOT return JSON
- Do NOT show raw data
- Be clear and human-friendly
- Follow company policy
- If info missing → ask user
"""

            final_text = generate(final_prompt).strip()

        elif action == "final":
            final_text = data.get("response", "No response generated")

        else:
            return {
                "error": "Unknown action from LLM",
                "raw": data
            }

        # 🚨 STEP 4 — Escalation logic
        should_escalate = False

        if any(word in user_input.lower() for word in ["broken", "defect", "warranty"]):
            should_escalate = True

        if "replace" in user_input.lower():
            should_escalate = True

        escalation_data = None

        if should_escalate:
            escalation_data = TOOLS["escalate_ticket"](
                "Complex issue requires human review"
            )

        # 🧠 STEP 5 — Save memory
        history.append(f"User: {user_input}")
        history.append(f"AI: {final_text}")

        chat_memory[session_id] = history[-10:]

        # 🔥 FINAL OUTPUT
        return {
            "response": final_text,
            "confidence": 0.8,  # static for now (no extra API call)
            "escalation": escalation_data
        }

    except Exception as e:
        return {"error": str(e)}