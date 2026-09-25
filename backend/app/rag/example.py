"""Standalone RAG example.

Run from the backend directory after installing the RAG dependency:

    python -m app.rag.example

This example does not modify or import Engineer Pulse controllers, business
services, data services, models, or main.py.
"""

from .rag_config import DOCUMENTS_DIR
from .rag_service import RAGService


def main():
    rag = RAGService()

    indexed = rag.ingest_directory(DOCUMENTS_DIR)
    print(f"Indexed chunks: {indexed}")

    result = rag.retrieve(
        query="What are common engineering challenges and AI opportunities?",
        top_k=3,
    )

    print("\nRetrieved content:")
    for item in result["results"]:
        print(f"\n[{item['id']}]")
        print(item["content"])
        print(f"Metadata: {item['metadata']}")


if __name__ == "__main__":
    main()
