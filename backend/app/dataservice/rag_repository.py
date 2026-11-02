"""RAG (Retrieval-Augmented Generation) data-access layer.

Embeds a user query and retrieves the most semantically similar documents
from the `vector_documents` table using pgvector cosine similarity.
Falls back to an empty list if the DB or pgvector is unavailable so the
chatbot continues to function (without context) rather than crashing.
"""
from __future__ import annotations

import hashlib
import logging
import os

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

EMBEDDING_DIMENSION = 1536


# ---------------------------------------------------------------------------
# Embedding helper
# ---------------------------------------------------------------------------

def _embed_text(text_input: str) -> list[float]:
    """Return a 1536-dimensional embedding vector for *text_input*.

    Priority order:
    1. OpenAI ``text-embedding-3-small`` if OPENAI_API_KEY is set.
    2. Deterministic dummy derived from an MD5 hash (works without any key).
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=openai_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text_input,
            )
            return response.data[0].embedding
        except Exception as exc:
            logger.warning("OpenAI embedding failed, falling back to dummy: %s", exc)

    # Deterministic dummy: same text -> same vector so cosine similarity
    # still makes sense within the seeded dataset.
    digest = hashlib.md5(text_input.encode()).hexdigest()
    seed = int(digest, 16)
    vector: list[float] = []
    for _ in range(EMBEDDING_DIMENSION):
        seed = (seed * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        vector.append(((seed >> 17) & 0xFFFF) / 32768.0 - 1.0)
    return vector


# ---------------------------------------------------------------------------
# Repository
# ---------------------------------------------------------------------------

class RAGRepository:
    """Retrieves knowledge from multiple pgvector tables for RAG context."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """Embed *query* and return the top-*top_k* matching documents.

        Searches across four tables:
        - vector_documents  (knowledge base articles)
        - employee_skills   (skill profiles)
        - employee_projects (project experience)
        - employee_feedback (peer reviews)

        Each result dict contains: ``title``, ``category``, ``content``.
        Returns an empty list on any failure so the caller degrades gracefully.
        """
        try:
            query_vec = _embed_text(query)
            vec_str = str(query_vec)

            # Union across all embedding tables, ranked by cosine distance
            sql = text("""
                (
                    SELECT title, category, content,
                           embedding <=> CAST(:vec AS vector) AS dist
                    FROM vector_documents
                    WHERE embedding IS NOT NULL
                    ORDER BY dist LIMIT :top_k
                )
                UNION ALL
                (
                    SELECT
                        employee_name || ' - ' || skill_name AS title,
                        'employee_skill' AS category,
                        employee_name || ' has ' || proficiency_level
                            || ' proficiency in ' || skill_name
                            || ' with ' || years_of_experience || ' years experience.' AS content,
                        embedding <=> CAST(:vec AS vector) AS dist
                    FROM employee_skills
                    WHERE embedding IS NOT NULL
                    ORDER BY dist LIMIT :top_k
                )
                UNION ALL
                (
                    SELECT
                        employee_name || ' - ' || project_name AS title,
                        'employee_project' AS category,
                        employee_name || ' worked as ' || role
                            || ' on project ' || project_name
                            || ' using ' || technologies
                            || '. ' || description AS content,
                        embedding <=> CAST(:vec AS vector) AS dist
                    FROM employee_projects
                    WHERE embedding IS NOT NULL
                    ORDER BY dist LIMIT :top_k
                )
                UNION ALL
                (
                    SELECT
                        employee_name || ' feedback from ' || reviewer_name AS title,
                        'employee_feedback' AS category,
                        reviewer_name || ' reviewed ' || employee_name
                            || ' (Rating: ' || rating || '/5): '
                            || feedback_text AS content,
                        embedding <=> CAST(:vec AS vector) AS dist
                    FROM employee_feedback
                    WHERE embedding IS NOT NULL
                    ORDER BY dist LIMIT :top_k
                )
                ORDER BY dist
                LIMIT :top_k
            """)
            rows = self._db.execute(
                sql,
                {"vec": vec_str, "top_k": top_k},
            ).fetchall()
            return [
                {"title": r.title, "category": r.category, "content": r.content}
                for r in rows
            ]
        except (OperationalError, ProgrammingError) as exc:
            logger.warning("RAG vector search unavailable (pgvector missing?): %s", exc)
            return []
        except Exception as exc:
            logger.warning("RAG retrieve error: %s", exc)
            return []

