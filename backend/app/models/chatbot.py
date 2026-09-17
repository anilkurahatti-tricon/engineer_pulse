"""Pydantic schemas for the Chatbot controller."""
from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessageBase(BaseModel):
    session_id: str = Field(..., examples=["session-001"])
    sender: str = Field(..., examples=["user"])
    message: str = Field(..., examples=["What is my current skill rating?"])


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageUpdate(BaseModel):
    message: str | None = None


class ChatMessage(ChatMessageBase):
    id: int
    created_at: datetime


class ChatAskRequest(BaseModel):
    session_id: str = Field(..., examples=["session-001"])
    message: str = Field(..., examples=["Summarize my recent feedback."])


class ChatAskResponse(BaseModel):
    session_id: str
    reply: str
    provider: str
    is_dummy_response: bool
