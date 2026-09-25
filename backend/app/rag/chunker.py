"""Simple, provider-independent text chunking."""

from dataclasses import dataclass


@dataclass
class TextChunker:
    chunk_size: int = 800
    chunk_overlap: int = 100

    def __post_init__(self):
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if self.chunk_overlap < 0 or self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk_overlap must be >= 0 and smaller than chunk_size"
            )

    def split(self, text: str) -> list[str]:
        text = " ".join(text.split())

        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])

            if end == len(text):
                break

            start = end - self.chunk_overlap

        return chunks
