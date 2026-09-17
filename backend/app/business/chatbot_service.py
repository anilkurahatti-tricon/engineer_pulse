"""Business logic layer for the Chatbot controller."""
from app.ai.ai_client import AIClient
from app.dataservice.chatbot_repository import ChatbotRepository, chatbot_repository
from app.models.chatbot import (
    ChatAskResponse,
    ChatMessage,
    ChatMessageCreate,
    ChatMessageUpdate,
)


class ChatbotService:
    """Business rules sit between the controller and data-access/AI layers."""

    def __init__(self, repository: ChatbotRepository) -> None:
        self._repository = repository

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
        """Persist the user message, get an AI reply, persist and return it."""
        self._repository.create(ChatMessageCreate(session_id=session_id, sender="user", message=message))
        reply, is_dummy = ai_client.generate_response(message)
        self._repository.create(ChatMessageCreate(session_id=session_id, sender="bot", message=reply))
        return ChatAskResponse(
            session_id=session_id,
            reply=reply,
            provider=ai_client.provider,
            is_dummy_response=is_dummy,
        )


def get_chatbot_service() -> ChatbotService:
    """FastAPI dependency factory for `ChatbotService`."""
    return ChatbotService(chatbot_repository)
