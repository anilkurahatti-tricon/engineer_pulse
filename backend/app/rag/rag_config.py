"""Optional configuration for the standalone RAG layer."""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
VECTOR_STORE_DIR = BASE_DIR / "data" / "vector_store"

DEFAULT_TOP_K = 5
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100
