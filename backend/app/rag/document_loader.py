"""Document loading utilities for the standalone RAG layer."""

from pathlib import Path


class DocumentLoader:
    """Load Markdown and text documents from a directory."""

    SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt"}

    def load_file(self, path: str | Path) -> dict:
        path = Path(path)

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported document type: {path.suffix}")

        return {
            "id": path.stem,
            "source": str(path),
            "text": path.read_text(encoding="utf-8"),
        }

    def load_directory(self, directory: str | Path) -> list[dict]:
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Document directory not found: {directory}")

        return [
            self.load_file(path)
            for path in sorted(directory.rglob("*"))
            if path.is_file()
            and path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]
