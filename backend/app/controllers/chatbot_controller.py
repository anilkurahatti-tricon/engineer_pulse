"""Chatbot controller: chat history CRUD plus an AI-powered /ask endpoint.

The `/ask` endpoint extracts AI provider configuration (API keys, model,
endpoint) from environment settings via the `AIClient` dependency and
processes the user's message through it.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.ai.ai_client import AIClient, get_ai_client
from app.business.chatbot_service import ChatbotService, get_chatbot_service
from app.models.chatbot import (
    ChatAskRequest,
    ChatAskResponse,
    ChatMessage,
    ChatMessageCreate,
    ChatMessageUpdate,
)

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])


@router.post("/ask", response_model=ChatAskResponse, summary="Send a message to the chatbot and get an AI reply")
def ask_chatbot(
    payload: ChatAskRequest,
    service: ChatbotService = Depends(get_chatbot_service),
    ai_client: AIClient = Depends(get_ai_client),
) -> ChatAskResponse:
    return service.ask(payload.session_id, payload.message, ai_client)


@router.get("/", response_model=list[ChatMessage], summary="List all chat messages")
def list_messages(service: ChatbotService = Depends(get_chatbot_service)) -> list[ChatMessage]:
    return service.list_messages()


@router.get("/{item_id}", response_model=ChatMessage, summary="Get a chat message by id")
def get_message(item_id: int, service: ChatbotService = Depends(get_chatbot_service)) -> ChatMessage:
    item = service.get_message(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat message not found")
    return item


@router.post(
    "/", response_model=ChatMessage, status_code=status.HTTP_201_CREATED, summary="Create a chat message"
)
def create_message(
    payload: ChatMessageCreate, service: ChatbotService = Depends(get_chatbot_service)
) -> ChatMessage:
    return service.create_message(payload)


@router.put("/{item_id}", response_model=ChatMessage, summary="Update a chat message")
def update_message(
    item_id: int,
    payload: ChatMessageUpdate,
    service: ChatbotService = Depends(get_chatbot_service),
) -> ChatMessage:
    item = service.update_message(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat message not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a chat message")
def delete_message(item_id: int, service: ChatbotService = Depends(get_chatbot_service)) -> None:
    if not service.delete_message(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat message not found")
