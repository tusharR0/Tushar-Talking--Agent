from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import run_agent  # import your AI logic

app = FastAPI()

# CORS for frontend (streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def chat_with_bot(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "")
        reply = run_agent(user_input)
        return {"response": reply}
    except Exception as e:
        return {"response": f"❌ Backend Error: {e}"}
