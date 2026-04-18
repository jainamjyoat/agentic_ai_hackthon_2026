
import json
from app.llm import MODEL, SYSTEM_PROMPT
from app.tools.tool_registry import TOOLS

# 🧠 SIMPLE MEMORY STORE (in-memory)
chat_memory = {}
def clean_llm_output(text: str):
    """
    Removes markdown formatting like ```json ... ```
    """
    text = text.strip()

    if "```" in text:
        text = text.replace("```json", "").replace("```", "").strip()

    return text


def run_agent(user_input: str, session_id: str = "default"):
    try:
        # 🔹 STEP 1: Ask LLM what to do
        prompt = SYSTEM_PROMPT + f"\nUser: {user_input}"

        response = MODEL.generate_content(prompt)
        text = clean_llm_output(response.text)

        try:
            data = json.loads(text)
        except Exception:
            return {
                "error": "Invalid LLM response",
                "raw": text
            }

        action = data.get("action")

        # 🔹 STEP 2: TOOL CALL
        if action in TOOLS:
            tool_fn = TOOLS[action]

            try:
                tool_result = tool_fn(**data.get("parameters", {}))
            except Exception as e:
                return {"error": f"Tool execution failed: {str(e)}"}

            # 🔥 STEP 3: FORCE FINAL RESPONSE
            final_prompt = f"""
You are a customer support AI.

User query:
{user_input}

Tool result:
{tool_result}

Now generate a FINAL response.

Rules:
- Do NOT assume missing information
- If something is required (like product condition), ASK the user
- Do NOT show raw data
- Be clear and professional
- Follow company policy strictly

If more info is needed → ask a question instead of deciding.
"""

            final_response = MODEL.generate_content(final_prompt)

            return final_response.text.strip()

        # 🔹 STEP 4: FINAL DIRECT RESPONSE
        if action == "final":
            return data.get("response", "No response generated")

        # 🔹 STEP 5: UNKNOWN ACTION
        return {
            "error": "Unknown action from LLM",
            "raw": data
        }

    except Exception as e:
        return {"error": str(e)}