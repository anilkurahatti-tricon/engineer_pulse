# Engineer Pulse — RAG Testing Guide

## 1. Purpose

This guide explains how to install, run, and test the standalone RAG (Retrieval-Augmented Generation) module in the Engineer Pulse backend.

The current RAG module is isolated under:

```text
backend/app/rag/
```

It does not require changes to the existing `ai`, `business`, `controllers`, `dataservice`, `models`, or `main.py` folders.

---

## 2. Current RAG Flow

```text
Knowledge Documents
       |
       v
Document Loader
       |
       v
Chunking
       |
       v
Embedding Model
       |
       v
ChromaDB Vector Store
       |
       v
Semantic Retrieval
       |
       v
Relevant Document Chunks
```

The current implementation is **retrieval only**. LLM-generated answers will be connected in the next phase.

---

## 3. Prerequisites

- Python 3.13.x
- Engineer Pulse backend
- Python virtual environment at `backend\.venv`
- Internet access for the first embedding-model download

---

## 4. Open the Backend

PowerShell:

```powershell
cd "C:\Users\mahadev\OneDrive - Tricon Infotech Pvt. Ltd\Documents\GitHub\engineer_pulse\backend"
```

Verify:

```powershell
pwd
```

---

## 5. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

Expected prompt:

```text
(.venv) PS C:\...\engineer_pulse\backend>
```

---

## 6. Install ChromaDB

Install:

```powershell
pip install chromadb
```

Verify:

```powershell
pip show chromadb
```

Or:

```powershell
python -c "import chromadb; print(chromadb.__version__)"
```

The current project was tested with ChromaDB 1.5.9.

---

## 7. RAG Folder Structure

```text
backend/
└── app/
    └── rag/
        ├── __init__.py
        ├── document_loader.py
        ├── chunker.py
        ├── embeddings.py
        ├── vector_store.py
        ├── retriever.py
        ├── rag_service.py
        ├── rag_config.py
        ├── example.py
        ├── query.py
        ├── README.md
        │
        └── data/
            └── documents/
                └── sample_engineer_pulse_knowledge.md
```

---

## 8. Sample Knowledge Document

The test document is:

```text
app/rag/data/documents/sample_engineer_pulse_knowledge.md
```

It contains sample information about:

- Engineering Quality
- Observability
- AI Engineering
- Team Feedback

You can add additional `.md`, `.markdown`, or `.txt` files to the same directory.

Example:

```text
app/rag/data/documents/
├── sample_engineer_pulse_knowledge.md
├── engineering_quality.md
├── observability.md
└── team_feedback.md
```

---

## 9. First Test — RAG Example

From the `backend` directory:

```powershell
python -m app.rag.example
```

Expected output will look similar to:

```text
Indexed chunks: 2

Retrieved content:
...
```

This confirms:

- Documents were loaded
- Documents were chunked
- Embeddings were generated
- ChromaDB was populated
- Retrieval worked

---

## 10. Interactive RAG Test

Run:

```powershell
python -m app.rag.query
```

Expected:

```text
============================================================
Engineer Pulse - RAG Query
Type 'exit' to quit
============================================================

Question:
```

Enter:

```text
What is observability?
```

The system should return retrieved chunks with their ID, distance, source, and content.

---

## 11. Recommended Test Questions

### Test 1 — Observability

```text
What is observability?
```

Expected topic:

```text
Observability
Application errors
Performance problems
Operational issues
Dashboards
Alerts
```

### Test 2 — Engineering Quality

```text
What are engineering quality practices?
```

Expected topic:

```text
Automated regression testing
Observability
Reliable environments
Continuous feedback
```

### Test 3 — AI Engineering

```text
How can AI help engineering teams?
```

Expected topic:

```text
AI assistants
Feedback summarization
Knowledge retrieval
Recurring themes
Contextual recommendations
```

### Test 4 — Team Feedback

```text
How can employee feedback be used?
```

Expected topic:

```text
Engineering processes
Tooling
Collaboration
Documentation
Automation
Delivery challenges
```

### Test 5 — Semantic Search

```text
What helps engineers detect production problems earlier?
```

Expected topic:

```text
Observability
Dashboards
Alerts
Production visibility
```

### Test 6 — Paraphrase

```text
How can a team identify application issues in production?
```

Expected topic:

```text
Observability
```

---

## 12. Negative Test

Try an unrelated question:

```text
How do I cook pasta?
```

or:

```text
What is the capital of France?
```

The returned chunks should be less relevant to Engineer Pulse knowledge.

This is a useful negative retrieval test.

---

## 13. How to Understand Distance

The query output contains a value such as:

```text
Distance : 1.4867
```

Distance represents how far the query embedding is from the retrieved document embedding according to the configured vector-space distance.

Generally:

```text
Lower distance
      ↓
More semantically similar

Higher distance
      ↓
Less semantically similar
```

Do not use one absolute distance value as a universal good/bad threshold. The useful test is whether the returned content is actually relevant.

---

## 14. Add Your Own Knowledge

Create a file such as:

```text
app/rag/data/documents/engineering_pulse_test.md
```

Example:

```markdown
# Engineer Pulse Test Knowledge

## API Quality

API quality can be improved through automated API testing,
contract validation, response-time monitoring, and error analysis.

## Automation

Automated regression testing helps teams detect defects
earlier and reduce repetitive manual testing.

## Monitoring

New Relic dashboards and alerts provide visibility into
application performance, errors, and operational health.
```

Then run:

```powershell
python -m app.rag.example
```

Test:

```text
What helps improve API quality?
```

and:

```text
How can automated testing help engineers?
```

---

## 15. Test Matrix

| Test | Question | Expected Topic | Purpose |
|---|---|---|---|
| T01 | What is observability? | Observability | Basic retrieval |
| T02 | What are engineering quality practices? | Quality | Topic retrieval |
| T03 | How can AI help engineering teams? | AI | Topic retrieval |
| T04 | How can employee feedback be used? | Feedback | Topic retrieval |
| T05 | What helps detect production problems earlier? | Observability | Semantic search |
| T06 | How can a team identify application issues? | Observability | Paraphrase |
| T07 | What improves API quality? | API testing | New document |
| T08 | How does automation help engineers? | Automation | New document |
| T09 | What is unrelated to Engineer Pulse? | Low relevance | Negative test |
| T10 | How can monitoring improve operations? | Monitoring | Semantic search |

---

## 16. End-to-End Test Checklist

### Step 1

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 2

```powershell
python -c "import chromadb; print(chromadb.__version__)"
```

### Step 3

```powershell
python -m app.rag.example
```

Verify:

```text
Indexed chunks: ...
```

### Step 4

```powershell
python -m app.rag.query
```

### Step 5

Test:

```text
What is observability?
```

### Step 6

Test semantic search:

```text
What helps engineers detect production problems earlier?
```

### Step 7

Test unrelated content:

```text
How do I cook pasta?
```

### Step 8

Exit:

```text
exit
```

---

## 17. First Run and Embedding Model Download

On the first RAG execution, Chroma may download:

```text
all-MiniLM-L6-v2
```

This is expected.

The model is cached locally, so later runs normally do not need to download it again.

---

## 18. Do We Need to Start Chroma Separately?

**No.**

The current implementation uses Chroma's persistent client directly from Python.

You do **not** need to start a separate Chroma server for this implementation.

Conceptually:

```text
Python RAG Application
        |
        v
Persistent Chroma Client
        |
        v
Local Vector Database
```

---

## 19. Current RAG Limitation

Current implementation:

```text
Question
   ↓
Embedding
   ↓
Chroma Search
   ↓
Relevant Chunks
   ↓
Display Results
```

It is not yet:

```text
Question
   ↓
RAG Retrieval
   ↓
LLM
   ↓
AI Answer
```

The next phase will connect retrieved context to:

```text
app/ai/ai_client.py
```

so Engineer Pulse can produce grounded AI answers.

---

## 20. Troubleshooting

### `ModuleNotFoundError: No module named 'chromadb'`

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
pip install chromadb
```

### `No module named app`

Make sure you are running from:

```text
backend/
```

Correct:

```powershell
cd ...\engineer_pulse\backend
python -m app.rag.query
```

### Query exits immediately

Check:

```powershell
Get-Content .\app\rag\query.py
```

The file should contain the interactive loop and:

```python
if __name__ == "__main__":
    main()
```

Then run:

```powershell
python -m app.rag.query
```

### No documents retrieved

Check:

```text
app/rag/data/documents/
```

Make sure the document exists, for example:

```text
sample_engineer_pulse_knowledge.md
```

Then run:

```powershell
python -m app.rag.example
```

---

## 21. Useful Daily Commands

Activate environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Check Chroma:

```powershell
pip show chromadb
```

Run RAG example:

```powershell
python -m app.rag.example
```

Run interactive RAG:

```powershell
python -m app.rag.query
```

Check Python:

```powershell
python --version
```

Check packages:

```powershell
pip list
```

---

## 22. Next Phase

Once retrieval testing is stable:

```text
                 Engineer Pulse RAG
                        |
                        v
                 User Question
                        |
                        v
                 Chroma Retrieval
                        |
                        v
                Relevant Context
                        |
                        v
                 AI Client
              app/ai/ai_client.py
                        |
                        v
                 Grounded Answer
                        |
                        v
                 Source References
```

Then:

```text
FastAPI Endpoint
       ↓
React UI
       ↓
Engineer Pulse AI Assistant
```

Development progression:

```text
Phase 1  → RAG Retrieval              Current
Phase 2  → RAG + LLM Answer           Next
Phase 3  → FastAPI RAG API            Later
Phase 4  → React UI                   Later
Phase 5  → Engineer Pulse AI Assistant
```

---

# Quick Start

For day-to-day testing:

```powershell
cd "C:\Users\mahadev\OneDrive - Tricon Infotech Pvt. Ltd\Documents\GitHub\engineer_pulse\backend"

.\.venv\Scripts\Activate.ps1

python -c "import chromadb; print(chromadb.__version__)"

python -m app.rag.example

python -m app.rag.query
```

Then test:

```text
Question: What is observability?
```

Use the test matrix above for additional validation.
