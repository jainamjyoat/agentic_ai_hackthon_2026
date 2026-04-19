from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

from app.agent import run_agent

app = FastAPI()

# 🧠 In-memory storage for uploaded JSON
uploaded_data = {}


# ✅ CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📦 Request schema
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# 🟢 Health check route
@app.get("/")
def root():
    return {"status": "AI Agent Running"}


# 📂 JSON Upload endpoint
@app.post("/upload-json")
async def upload_json(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        data = json.loads(contents)

        uploaded_data["data"] = data

        return {
            "status": "success",
            "message": "JSON uploaded successfully"
        }

    except Exception as e:
        return {"error": str(e)}


# 💬 Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = run_agent(
            req.message,
            req.session_id,
            external_data=uploaded_data.get("data")  # 🔥 pass JSON
        )
        return result
    except Exception as e:
        return {"error": str(e)}