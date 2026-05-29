from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    tools_called: list[str]

@router.post("/chat", response_model = ChatResponse)
def chat(req: ChatRequest):
    result = run_agent(req.message)
    return ChatResponse(
        reply = result.get("reply", ""),
        tools_called = result.get("tools_called", []),
    )