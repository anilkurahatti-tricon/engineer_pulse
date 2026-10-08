# Backend (FastAPI)

Layered structure:

```
backend/
  agents/        # LangChain + Groq AI agents (gap analysis, roadmap)
  app/
    controllers/   # API layer (FastAPI routers) - request/response only
    business/      # business logic / services
    dataservice/   # data access layer (PostgreSQL via SQLAlchemy)
    models/        # Pydantic request/response schemas
    ai/            # pluggable AI client (OpenAI / Azure OpenAI), reads .env
    core/          # settings/config (.env loading)
    main.py        # FastAPI app entrypoint
  scripts/
    setup_postgres_vector.py  # DB setup + seed script (run once per local DB)
  requirements.txt
  .env.example
```

---

## Setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

---

## Database — choose one option

### Option A — Shared Supabase (team / cloud DB)

Get the `DATABASE_URL` from your squad lead and paste it in `.env`:

```env
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:5432/<dbname>?sslmode=require
```

Skip the Docker and seed steps — the shared DB is already configured.

---

### Option B — Your own local DB (Docker)

> Each developer runs their own isolated PostgreSQL + pgvector instance locally.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

**Step 1 — Start the database container** (from the repo root, not `backend/`):

```powershell
docker compose up -d
```

This spins up `pgvector/pgvector:pg16` on `localhost:5432` with:
- DB name: `engineer_pulse`
- User: `postgres`
- Password: `postgres`

**Step 2 — Point `.env` at your local DB** (leave `DATABASE_URL` blank):

```env
DATABASE_URL=

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=engineer_pulse
```

**Step 3 — Create tables, indexes, and seed data** (run once):

```powershell
# from backend/
.venv\Scripts\python.exe scripts/setup_postgres_vector.py
```

Options:
```
--dry-run    validate config only, no DB changes
--recreate   DROP and recreate all tables  ⚠️ destructive
```

**Stop / reset:**
```powershell
docker compose down        # stop container (data preserved)
docker compose down -v     # stop + delete all data
```

---

## AI Provider Setup

Add your Groq API key to `.env` — required for the gap-analysis and roadmap agents:

```env
GROQ_API_KEY=gsk_...
```

Optionally configure OpenAI / Azure OpenAI for the chatbot endpoint:

```env
OPENAI_API_KEY=sk-...
```

---

## Run

```powershell
# from backend/
uvicorn app.main:app --reload --port 8000
```

---

## Swagger / API docs

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI — interactive, try endpoints live |
| http://localhost:8000/redoc | ReDoc — read-only docs |
| http://localhost:8000/openapi.json | Raw OpenAPI schema |

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/gap-analysis/analyze` | `POST` | AI skill-gap analysis for an employee vs projects |
| `/api/roadmap/generate` | `POST` | AI upskilling roadmap from a gap-analysis result |
| `/api/employee-skills` | `GET/POST` | Employee skill CRUD |
| `/api/employee-feedback` | `GET/POST` | Employee feedback CRUD |
| `/api/chatbot/ask` | `POST` | AI chatbot (OpenAI / Azure OpenAI) |
| `/api/welcome` | `GET` | App landing-page content |
| `/api/demo` | `GET/POST` | Sandbox CRUD demo |

### Gap Analysis example

```json
POST /api/gap-analysis/analyze
{
  "employee_id": 1,
  "project_ids": [2, 3]
}
```

Use `GET /api/employee-skills` to discover valid employee IDs, and query the `employee_projects` table for project IDs.
