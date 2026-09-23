"""High-level RAG service.

Application code should interact with RAGService rather than directly with
the vector database, chunker, or document loader.
"""

from pathlib import Path

from .chunker import TextChunker
from .document_loader import DocumentLoader
from .retriever import Retriever
from .vector_store import ChromaVectorStore


class RAGService:
    def __init__(
        self,
        vector_store=None,
        document_loader=None,
        chunker=None,
    ):
        self.vector_store = vector_store or ChromaVectorStore()
        self.document_loader = document_loader or DocumentLoader()
        self.chunker = chunker or TextChunker()
        self.retriever = Retriever(self.vector_store)

    def ingest_directory(self, directory: str | Path) -> int:
        """Load, chunk, and index all supported documents."""
        documents = self.document_loader.load_directory(directory)
        indexed_chunks = 0

        for document in documents:
            chunks = self.chunker.split(document["text"])

            ids = [
                f'{document["id"]}-chunk-{index}'
                for index in range(len(chunks))
            ]

            metadata = [
                {
                    "document_id": document["id"],
                    "source": document["source"],
                    "chunk_index": index,
                }
                for index in range(len(chunks))
            ]

            self.vector_store.upsert(
                documents=chunks,
                ids=ids,
                metadatas=metadata,
            )

            indexed_chunks += len(chunks)

        return indexed_chunks

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """Retrieve semantically relevant content."""
        results = self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        return {
            "query": query,
            "count": len(results),
            "results": results,
        }
