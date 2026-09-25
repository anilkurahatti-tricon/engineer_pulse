# Engineer Pulse - Standalone RAG Layer

This folder is intentionally isolated from the existing Engineer Pulse
application.

## Location

Place this folder here:

```text
backend/app/rag/
```

No existing `ai`, `business`, `controllers`, `dataservice`, `models`, or
`main.py` files need to be changed.

## Purpose

The RAG layer provides:

1. Document loading
2. Text chunking
3. Embedding/vector-store abstraction
4. Semantic retrieval
5. A reusable `RAGService`

## Current POC flow

```text
Documents
   ↓
DocumentLoader
   ↓
TextChunker
   ↓
Chroma Vector Store
   ↓
Retriever
   ↓
RAGService
   ↓
Relevant Context
```

## Installation

Add Chroma to the existing backend environment:

```text
chromadb
```

or install the included dependency file:

```bash
pip install -r requirements-rag.txt
```

## Test without changing the application

From the `backend` directory:

```bash
python -m app.rag.example
```

This indexes the sample document and performs a semantic search.

## Later integration

When the POC is ready, the existing business/controller layers can call:

```python
from app.rag.rag_service import RAGService

rag = RAGService()

result = rag.retrieve(
    query="What are the engineering challenges?",
    top_k=5,
)
```

The RAG layer can later be connected to the existing `ai_client.py` so the
retrieved context is passed to the LLM for a grounded response.

## Future extensions

- PDF/document loaders
- Database-backed knowledge
- Metadata filtering
- OpenAI/Azure OpenAI embeddings
- PostgreSQL + pgvector
- Reranking
- RAG evaluation
- LLM response generation
- Engineer Pulse feedback retrieval
