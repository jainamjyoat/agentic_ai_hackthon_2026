import json
from app.llm import MODEL, SYSTEM_PROMPT
from app.tools.tool_registry import TOOLS

# 🧠 In-memory chat memory
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
        # 🧠 LOAD MEMORY
        history = chat_memory.get(session_id, [])
        history_text = "\n".join(history)

        # 🔹 STEP 1: Ask LLM what to do
        prompt = SYSTEM_PROMPT + f"""
Conversation history:
{history_text}

User: {user_input}
"""

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

            # 🔥 STEP 3: FINAL RESPONSE (LLM INTERPRETATION)
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
- Be polite and human-friendly
- Follow company policy
- If information is missing, ask the user instead of assuming
- Clearly state decision (approved / rejected / needs more info)
"""

            final_response = MODEL.generate_content(final_prompt)
            final_text = final_response.text.strip()

        # 🔹 STEP 4: DIRECT FINAL
        elif action == "final":
            final_text = data.get("response", "No response generated")

        else:
            return {
                "error": "Unknown action from LLM",
                "raw": data
            }

        # 📊 STEP 5: CONFIDENCE SCORE
        confidence_prompt = f"""
Evaluate confidence of this response.

User: {user_input}
Response: {final_text}

Return ONLY a number between 0 and 1.
"""

        confidence_raw = MODEL.generate_content(confidence_prompt).text.strip()

        try:
            confidence = float(confidence_raw)
        except:
            confidence = 0.5

        # 🚨 STEP 6: ESCALATION LOGIC
        should_escalate = False

        if confidence < 0.6:
            should_escalate = True

        if any(word in user_input.lower() for word in ["broken", "defect", "warranty"]):
            should_escalate = True

        if "replace" in user_input.lower():
            should_escalate = True

        escalation_data = None

        if should_escalate:
            escalation_data = TOOLS["escalate_ticket"](
                "Complex issue requires human review"
            )

        # 🧠 STEP 7: SAVE MEMORY
        history.append(f"User: {user_input}")
        history.append(f"AI: {final_text}")

        chat_memory[session_id] = history[-10:]

        # 🔥 FINAL OUTPUT
        return {
            "response": final_text,
            "confidence": confidence,
            "escalation": escalation_data
        }

    except Exception as e:
        return {"error": str(e)}