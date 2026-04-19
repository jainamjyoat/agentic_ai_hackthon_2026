#  AI Support Agent (Full Stack)

An intelligent AI-powered customer support system that handles refund queries, processes user-uploaded data, and simulates real-world support workflows.

---

##  Features

*  AI Chat-based Support System
*  Upload Custom JSON Data (Dynamic Knowledge Base)
*  Refund Eligibility Checking
*  Tool-based Agent (Order + Refund + Escalation)
*  Session Memory Support
*  Interactive UI (Yes/No actions for refund processing)
*  Full-stack Deployment (Frontend + Backend)

---

##  Tech Stack

### Backend

* Python (FastAPI)
* Uvicorn
* Tool-based Agent Architecture
* JSON-based dynamic data

### Frontend

* Next.js (TypeScript)
* Tailwind CSS

### AI

* LLM (Gemini / Mistral depending on setup)
* Custom Agent Logic (no hardcoding)

### Deployment

* Backend → Render
* Frontend → Vercel
* Docker (optional)

---

##  Project Structure

backend/
│── app/
│ ├── main.py
│ ├── agent.py
│ ├── llm.py
│ ├── tools/
│ │ ├── order_tool.py
│ │ ├── refund_tool.py
│ │ ├── escalation_tool.py
│ │ └── tool_registry.py
│ └── data/
│
frontend/
│── app/
│ ├── page.tsx
│ ├── api/
│ │ ├── chat/
│ │ └── upload/

---

##  Setup Instructions

### 1️ Clone the Repository

```bash
git clone <your-repo-url>
cd your-project
```

---

### 2️ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

### 3️ Add Environment Variables

Create `.env` file inside backend:

```env
GEMINI_API_KEY=your_api_key
```

(OR use Mistral if configured)

---

### 4️ Run Backend

```bash
python -m uvicorn app.main:app --reload
```

Backend will run on:

```
http://127.0.0.1:8000
```

Docs available at:

```
http://127.0.0.1:8000/docs
```

---

### 5️ Frontend Setup

```bash
cd frontend
npm install
```

---

### 6️ Frontend Environment

Create `.env.local`:

```env
BACKEND_URL=http://127.0.0.1:8000/chat
```

---

### 7️⃣ Run Frontend

```bash
npm run dev
```

Frontend runs on:

```
http://localhost:3000
```

---

## 🧪 How to Use

### Step 1: Upload JSON Data

Use UI or `/upload-json` endpoint to upload:

```json
{
  "orders": [
    {
      "order_id": "ORD-777",
      "status": "delivered",
      "amount": 150,
      "return_deadline": "2099-12-30"
    }
  ],
  "products": [
    {
      "product_id": "P001",
      "name": "Wireless Headphones",
      "returnable": true
    }
  ]
}
```

---

### Step 2: Ask Queries

Example:

```
refund for ORD-777
```

---

### Step 3: Interact

* AI checks eligibility
* Shows response
* Offers action buttons
* Processes refund

---

## API Endpoints

| Method | Endpoint       | Description     |
| ------ | -------------- | --------------- |
| GET    | `/`            | Health check    |
| POST   | `/chat`        | Chat with agent |
| POST   | `/upload-json` | Upload data     |

---

##  Agent Workflow

1. User sends query
2. Agent extracts intent
3. Tool is selected (refund/order/etc.)
4. Tool processes data
5. AI generates final response
6. Optional escalation triggered

---

##  Deployment

### Backend (Render)

* Add `python-multipart` in requirements
* Set start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

### Frontend (Vercel)

Set environment variable:

```env
BACKEND_URL=https://your-render-url.onrender.com/chat
```

---

##  Important Notes

* No hardcoded data used
* Supports dynamic JSON upload
* Designed for real-world scalability

---

## Author

Built for Hackathon Project 

---

##  Future Improvements

* Database storage (persistent memory)
* Multi-user sessions
* Better UI/UX animations
* Payment/refund tracking

---