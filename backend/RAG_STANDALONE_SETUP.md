# Standalone RAG Setup

Extract the ZIP at the project root so that it creates:

```text
backend/app/rag/
```

For example:

```text
engineer_pulse/
└── backend/
    └── app/
        ├── ai/
        ├── business/
        ├── controllers/
        ├── core/
        ├── dataservice/
        ├── models/
        ├── rag/          <-- new, isolated
        └── main.py
```

Nothing inside the existing folders is replaced.

Add `chromadb` to `backend/requirements.txt` when you are ready to run the
RAG code, or use the included `requirements-rag.txt` for a separate install.

Test:

```bash
cd backend
python -m app.rag.example
```

Integration with existing Engineer Pulse code can be done later after the
standalone RAG flow is validated.
