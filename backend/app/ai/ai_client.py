"""AI integration layer - Groq-powered chatbot with optional RAG context injection.

The AIClient is used by the chatbot service. When a list of RAG context
documents is passed in, they are injected into the system prompt so the LLM
answers are grounded in real project/employee knowledge rather than generic
world knowledge.

Provider resolution order (first available wins):
    1. Groq  - if GROQ_API_KEY is set   (fast, free tier, already configured)
    2. OpenAI - if OPENAI_API_KEY is set
    3. Dummy  - deterministic echo, no credentials needed
"""
from __future__ import annotations

import logging
import os

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt template
# ---------------------------------------------------------------------------
_SYSTEM_PROMPT = """You are the Engineer Pulse AI Assistant - an intelligent HR and
engineering talent analytics assistant for the Engineer Pulse platform.

You help with:
- Employee skill profiles, gaps, and strengths
- Project assignments and technology requirements
- Feedback summaries and performance insights
- Upskilling roadmaps and career guidance

Answer concisely and professionally. Base your answers on the CONTEXT provided
when available. If the context does not contain enough information, say so
honestly rather than guessing.

{context_block}"""

_NO_CONTEXT = "(No additional context retrieved - answer from general knowledge.)"


def _build_system_prompt(context_docs: list[dict]) -> str:
    if not context_docs:
        return _SYSTEM_PROMPT.format(context_block=_NO_CONTEXT)
    blocks = []
    for doc in context_docs:
        blocks.append(
            "[{cat}] {title}\n{content}".format(
                cat=doc.get("category", "info").upper(),
                title=doc.get("title", ""),
                content=doc.get("content", ""),
            )
        )
    context_block = "CONTEXT (retrieved from the knowledge base):\n" + "\n\n".join(blocks)
    return _SYSTEM_PROMPT.format(context_block=context_block)


# ---------------------------------------------------------------------------
# AIClient
# ---------------------------------------------------------------------------

class AIClient:
    """Pluggable AI client that routes to Groq, OpenAI, or a dummy echo."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def provider(self) -> str:
        # Report which provider will actually be used
        if os.getenv("GROQ_API_KEY") or self._settings.groq_api_key:
            return "groq"
        if self._settings.openai_api_key:
            return "openai"
        return "dummy"

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate_response(
        self,
        prompt: str,
        context_docs: list[dict] | None = None,
    ) -> tuple[str, bool]:
        """Return (reply, is_dummy_response).

        Args:
            prompt:       The user's message.
            context_docs: RAG documents retrieved for this query. When
                          provided they are injected into the system prompt.
        """
        docs = context_docs or []
        system_prompt = _build_system_prompt(docs)

        # -- Groq (preferred - already configured in .env) --
        groq_key = os.getenv("GROQ_API_KEY") or self._settings.groq_api_key
        if groq_key:
            return self._call_groq(groq_key, system_prompt, prompt)

        # -- OpenAI --
        if self._settings.openai_api_key:
            return self._call_openai(system_prompt, prompt)

        # -- Dummy fallback --
        return (
            "[dummy] No AI key configured. You asked: '{p}'".format(p=prompt),
            True,
        )

    # ------------------------------------------------------------------
    # Provider implementations
    # ------------------------------------------------------------------

    def _call_groq(
        self, api_key: str, system_prompt: str, user_message: str
    ) -> tuple[str, bool]:
        try:
            from groq import Groq  # type: ignore
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=self._settings.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_message},
                ],
                temperature=0.4,
                max_tokens=1024,
            )
            reply = completion.choices[0].message.content or ""
            return reply.strip(), False
        except Exception as exc:
            logger.error("Groq API error: %s", exc)
            return "[groq-error] {e}".format(e=exc), True

    def _call_openai(self, system_prompt: str, user_message: str) -> tuple[str, bool]:
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=self._settings.openai_api_key)
            completion = client.chat.completions.create(
                model=self._settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_message},
                ],
                temperature=0.4,
                max_tokens=1024,
            )
            reply = completion.choices[0].message.content or ""
            return reply.strip(), False
        except Exception as exc:
            logger.error("OpenAI API error: %s", exc)
            return "[openai-error] {e}".format(e=exc), True


def get_ai_client() -> AIClient:
    """FastAPI dependency factory for AIClient."""
    return AIClient(get_settings())