"""Retrieval abstraction."""

from typing import Any


class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        return self.vector_store.search(
            query=query,
            top_k=top_k,
        )
