from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent  # ✅ FIXED: import without 'backend.'

app = FastAPI()

# CORS middleware to allow Streamlit frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your Streamlit URL
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
        return {"response": f"❌ Backend Error: {str(e)}"}
