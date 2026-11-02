"""Business logic layer for the Chatbot controller.

The ``ask`` method now implements the full RAG loop:
    1. Persist the user message.
    2. Retrieve semantically relevant documents from the vector_documents table
       (via RAGRepository).
    3. Pass those context documents to AIClient so they are injected into the
       LLM system prompt.
    4. Persist and return the grounded AI reply.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.ai.ai_client import AIClient
from app.core.database import get_db
from app.dataservice.chatbot_repository import ChatbotRepository, chatbot_repository
from app.dataservice.rag_repository import RAGRepository
from app.models.chatbot import (
    ChatAskResponse,
    ChatMessage,
    ChatMessageCreate,
    ChatMessageUpdate,
)


class ChatbotService:
    """Business rules sit between the controller and data-access/AI layers."""

    def __init__(self, repository: ChatbotRepository, db: Session) -> None:
        self._repository = repository
        self._db = db

    def list_messages(self) -> list[ChatMessage]:
        return self._repository.get_all()

    def get_message(self, item_id: int) -> ChatMessage | None:
        return self._repository.get_by_id(item_id)

    def create_message(self, payload: ChatMessageCreate) -> ChatMessage:
        return self._repository.create(payload)

    def update_message(self, item_id: int, payload: ChatMessageUpdate) -> ChatMessage | None:
        return self._repository.update(item_id, payload)

    def delete_message(self, item_id: int) -> bool:
        return self._repository.delete(item_id)

    def ask(self, session_id: str, message: str, ai_client: AIClient) -> ChatAskResponse:
        """Full RAG loop: retrieve context ? grounded LLM reply ? persist."""
        # 1. Persist user message
        self._repository.create(
            ChatMessageCreate(session_id=session_id, sender="user", message=message)
        )

        # 2. RAG retrieval — fetch top-4 relevant knowledge documents
        rag_repo = RAGRepository(self._db)
        context_docs = rag_repo.retrieve(message, top_k=4)

        # 3. Generate grounded reply (context injected into system prompt)
        reply, is_dummy = ai_client.generate_response(message, context_docs=context_docs)

        # 4. Persist bot reply
        self._repository.create(
            ChatMessageCreate(session_id=session_id, sender="bot", message=reply)
        )

        return ChatAskResponse(
            session_id=session_id,
            reply=reply,
            provider=ai_client.provider,
            is_dummy_response=is_dummy,
        )


def get_chatbot_service(db: Session = next(get_db())) -> ChatbotService:
    """FastAPI dependency factory for ``ChatbotService``."""
    return ChatbotService(chatbot_repository, db)
