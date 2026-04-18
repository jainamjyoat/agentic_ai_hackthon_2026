from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_agent

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = run_agent(req.message)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}