import streamlit as st # type: ignore
import requests # type: ignore
import os

# 🔗 Backend URL (from environment or default to localhost)
BACKEND_URL = "https://tushar-talking-agent.onrender.com"


# 🎨 Page setup
st.set_page_config(page_title="TailorTalk AI", layout="centered")
st.title("💬 Tushar's Appointment Bot")

# 💬 Initialize session message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Capture user input from chat
user_input = st.chat_input("Ask me to book a meeting...")

if user_input:
    # ➕ Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # 🚀 Send message to FastAPI backend
        response = requests.post(BACKEND_URL, json={"message": user_input})
        response.raise_for_status()

        # ✅ Get response content
        data = response.json()
        bot_reply = data.get("response", "⚠️ No 'response' key in backend reply.")

    except Exception as e:
        bot_reply = f"❌ Error contacting backend: {e}"

    # ➕ Add bot reply to chat history
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# 💬 Display full conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
