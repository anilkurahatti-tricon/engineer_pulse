"""Vector store adapter.

Chroma is used only inside this adapter so the rest of the RAG layer stays
independent of the vector database implementation.
"""

from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils import embedding_functions


class ChromaVectorStore:
    def __init__(
        self,
        collection_name: str = "engineer_pulse_rag",
        persist_directory: str | Path | None = None,
    ):
        if persist_directory is None:
            persist_directory = Path(__file__).resolve().parent / "data" / "vector_store"

        self.client = chromadb.PersistentClient(path=str(persist_directory))

        # Chroma's default embedding function keeps the initial POC local.
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
        )

    def upsert(
        self,
        documents: list[str],
        ids: list[str],
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        if not documents:
            return

        self.collection.upsert(
            documents=documents,
            ids=ids,
            metadatas=metadatas,
        )

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if not query.strip():
            raise ValueError("query must not be empty")

        result = self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )

        documents = result.get("documents", [[]])[0]
        ids = result.get("ids", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
            {
                "id": ids[index],
                "content": documents[index],
                "metadata": metadatas[index] or {},
                "distance": (
                    distances[index]
                    if index < len(distances)
                    else None
                ),
            }
            for index in range(len(documents))
        ]
