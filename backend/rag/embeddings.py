"""Embedding abstraction.

The RAG service does not depend directly on a specific embedding provider.
A future OpenAI, Azure OpenAI, Hugging Face, or local provider can implement
the same interface.

The default Chroma vector-store implementation manages embeddings internally.
"""

from typing import Protocol


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> list[float]:
        """Return an embedding vector for one piece of text."""
        ...


class EmbeddingService:
    """Provider-neutral wrapper for future embedding integrations."""

    def __init__(self, provider: EmbeddingProvider | None = None):
        self.provider = provider

    def embed(self, text: str) -> list[float]:
        if self.provider is None:
            raise RuntimeError(
                "No embedding provider configured. "
                "Use the vector store's built-in embedding function "
                "or provide an embedding provider."
            )

        return self.provider.embed(text)
