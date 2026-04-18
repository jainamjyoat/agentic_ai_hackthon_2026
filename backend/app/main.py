from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.agent import run_agent

app = FastAPI()


# ✅ CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📦 Request schema
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"   # 🧠 supports memory


# 🟢 Health check route
@app.get("/")
def root():
    return {"status": "AI Agent Running"}


# 💬 Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = run_agent(req.message, req.session_id)
        return result
    except Exception as e:
        return {"error": str(e)}