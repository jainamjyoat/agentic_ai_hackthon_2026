import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

# ✅ Fast + cheap model
MODEL_NAME = "mistral-small-latest"


def generate(prompt: str) -> str:
    response = client.chat.complete(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


SYSTEM_PROMPT = """
You are an AI customer support agent.

You must:
- Understand user intent
- Extract order_id if present
- Decide which tool to call

Respond ONLY in JSON format:

{
  "action": "tool_name OR final",
  "parameters": {},
  "response": ""
}
"""