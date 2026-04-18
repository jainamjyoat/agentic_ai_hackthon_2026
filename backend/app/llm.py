import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

MODEL_NAME = "mistral-small-latest"


def generate(prompt: str) -> str:
    response = client.beta.conversations.start(
        model=MODEL_NAME,
        inputs=[
            {"role": "user", "content": prompt}
        ]
    )
    print(response.outputs[0].content)
    return response.outputs[0].content


SYSTEM_PROMPT = """
You are an AI customer support agent.

Respond ONLY in JSON format:
{
  "action": "tool_name OR final",
  "parameters": {},
  "response": ""
}
"""