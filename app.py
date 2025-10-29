import os
import uuid
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


from inference import TechSupportChatbot


app = FastAPI(title="Tech Support Chatbot API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DEFAULT_MODEL_ID = os.getenv("HF_MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
BACKEND = os.getenv("BACKEND", "vllm").lower()
TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))


_sessions: Dict[str, TechSupportChatbot] = {}


def get_or_create_bot(session_id: Optional[str]):
    """
    Returns (session_id, bot). If session_id is None/unknown, It create new session.
    """
    if not session_id or session_id not in _sessions:
        # Create a new session
        sid = session_id or str(uuid.uuid4())
        _sessions[sid] = TechSupportChatbot(
            model_id=DEFAULT_MODEL_ID,
            hf_token=HF_TOKEN,
            top_k=TOP_K,
        )
        return sid, _sessions[sid]
    return session_id, _sessions[session_id]



class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the assistant.")
    session_id: Optional[str] = Field(
        None, description="Use the same session_id to continue a conversation."
    )


class ChatResponse(BaseModel):
    session_id: str
    reply: str


class ResetRequest(BaseModel):
    session_id: Optional[str] = None


class ResetResponse(BaseModel):
    session_id: str
    status: str = "cleared"



@app.get("/health")
def health():
    return {
        "status": "ok",
        "backend": BACKEND,
        "model_id": DEFAULT_MODEL_ID,
        "sessions": len(_sessions),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Create or retrieve session
    sid, bot = get_or_create_bot(req.session_id)

    # Basic guard
    msg = (req.message or "").strip()
    if not msg:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    # Chat
    try:
        reply = bot.chat(msg)
    except Exception as e:
        # Surface a clean error while keeping logs server-side
        raise HTTPException(status_code=500, detail=f"generation_error: {e}")

    return ChatResponse(session_id=sid, reply=reply)


@app.post("/reset", response_model=ResetResponse)
def reset(req: ResetRequest):
    sid, bot = get_or_create_bot(req.session_id)
    bot.reset()
    return ResetResponse(session_id=sid, status="cleared")


# Optional: if you want to run `python app.py`
if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    # reload=False avoids double-loading with some CUDA/vLLM setups
    uvicorn.run("app:app", host=host, port=port, reload=False, log_level="info")
    