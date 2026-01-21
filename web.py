from pathlib import Path
import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import MEMORY_FILE
from core.brain import think
from core.memory import add_to_memory, load_memory, save_memory
from core.security import is_safe

app = FastAPI(title="AI Assistant Web", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


memory_lock = threading.Lock()
memory = load_memory(MEMORY_FILE)


@app.post("/api/chat")
def chat(req: ChatRequest):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    if not is_safe(message):
        return {"reply": "That request is blocked for safety."}

    try:
        with memory_lock:
            global memory
            memory = add_to_memory(memory, "user", message)
            reply = think(memory)
            memory = add_to_memory(memory, "assistant", reply)
            save_memory(MEMORY_FILE, memory)

        return {"reply": reply, "memory_length": len(memory)}
    except Exception as e:
        error_msg = str(e)
        return {"reply": f"Error: {error_msg}", "error": True}


@app.get("/health")
def health():
    return {"status": "ok"}


static_dir = Path(__file__).parent / "frontend"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
