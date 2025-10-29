import os
import requests
import streamlit as st
from typing import Optional

# -----------------------------
# Config
# -----------------------------
DEFAULT_API_BASE = os.getenv("CHATBOT_API_BASE", "http://34.30.57.33:8000")
TIMEOUT_SECS = 120

# -----------------------------
# Helpers
# -----------------------------
def api_health(api_base: str):
    try:
        r = requests.get(f"{api_base}/health", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": f"error: {e}"}

def api_chat(api_base: str, message: str, session_id: Optional[str]):
    payload = {"message": message, "session_id": session_id}
    r = requests.post(f"{api_base}/chat", json=payload, timeout=TIMEOUT_SECS)
    r.raise_for_status()
    return r.json()

def api_reset(api_base: str, session_id: Optional[str]):
    payload = {"session_id": session_id}
    r = requests.post(f"{api_base}/reset", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Tech Support Chatbot", page_icon="💬", layout="centered")

with st.sidebar:
    st.header("⚙️ Settings")
    api_base = st.text_input("API Base URL", value=DEFAULT_API_BASE, help="Your FastAPI server base URL.")
    colA, colB = st.columns(2)
    with colA:
        if st.button("🔁 Health Check"):
            st.session_state["health"] = api_health(api_base)
    with colB:
        if st.button("🧹 Reset Session"):
            try:
                sid = st.session_state.get("session_id")
                api_reset(api_base, sid)
            except Exception as e:
                st.warning(f"Reset error: {e}")
            # Clear local state
            st.session_state["session_id"] = None
            st.session_state["messages"] = []
            st.toast("Session reset", icon="✅")

    st.divider()
    h = st.session_state.get("health")
    if h:
        st.caption("Health")
        st.json(h, expanded=False)

st.title("💬 Tech Support Chatbot")

# Initialize state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None

# Chat history render
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Type your message…")

if prompt:
    # Show user message immediately
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            resp = api_chat(api_base, prompt.strip(), st.session_state.get("session_id"))
            # Persist server-provided session id
            st.session_state["session_id"] = resp.get("session_id", st.session_state.get("session_id"))
            reply = resp.get("reply", "")
            placeholder.markdown(reply)
            st.session_state["messages"].append({"role": "assistant", "content": reply})
        except requests.HTTPError as e:
            try:
                detail = e.response.json().get("detail")
            except Exception:
                detail = str(e)
            placeholder.error(f"Server error: {detail}")
        except Exception as e:
            placeholder.error(f"Request failed: {e}")