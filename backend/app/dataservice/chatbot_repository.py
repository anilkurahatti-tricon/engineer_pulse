"""In-memory data access layer for the Chatbot controller (chat history)."""
from datetime import datetime, timezone
from itertools import count

from app.models.chatbot import ChatMessage, ChatMessageCreate, ChatMessageUpdate

_id_generator = count(start=1)

_chat_store: dict[int, ChatMessage] = {}


def _seed() -> None:
    seed_rows = [
        ("session-001", "user", "Hi, what can you help me with?"),
        ("session-001", "bot", "I can help you review feedback and skills data."),
    ]
    for session_id, sender, message in seed_rows:
        item_id = next(_id_generator)
        _chat_store[item_id] = ChatMessage(
            id=item_id,
            session_id=session_id,
            sender=sender,
            message=message,
            created_at=datetime.now(timezone.utc),
        )


_seed()


class ChatbotRepository:
    """Data-access operations for chat messages (dummy in-memory store)."""

    def get_all(self) -> list[ChatMessage]:
        return list(_chat_store.values())

    def get_by_id(self, item_id: int) -> ChatMessage | None:
        return _chat_store.get(item_id)

    def create(self, payload: ChatMessageCreate) -> ChatMessage:
        item_id = next(_id_generator)
        item = ChatMessage(id=item_id, created_at=datetime.now(timezone.utc), **payload.model_dump())
        _chat_store[item_id] = item
        return item

    def update(self, item_id: int, payload: ChatMessageUpdate) -> ChatMessage | None:
        existing = _chat_store.get(item_id)
        if existing is None:
            return None
        updated_data = existing.model_dump()
        updated_data.update({k: v for k, v in payload.model_dump().items() if v is not None})
        updated_item = ChatMessage(**updated_data)
        _chat_store[item_id] = updated_item
        return updated_item

    def delete(self, item_id: int) -> bool:
        return _chat_store.pop(item_id, None) is not None


chatbot_repository = ChatbotRepository()
