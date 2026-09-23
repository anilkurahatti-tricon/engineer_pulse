# Backend (FastAPI)

Layered structure:

```
backend/
  app/
    controllers/   # API layer (FastAPI routers) - request/response only
    business/      # business logic / services
    dataservice/    # data access layer (in-memory dummy stores for now)
    models/        # Pydantic request/response schemas
    ai/            # pluggable AI client (OpenAI / Azure OpenAI), reads .env
    core/          # settings/config (.env loading)
    main.py        # FastAPI app entrypoint
  requirements.txt
  .env.example
```

## Setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

**Database Setup**:
1. Get the `DATABASE_URL` for the shared Supabase project from your squad lead.
2. Open `.env` and set `DATABASE_URL=postgresql+psycopg2://...`
3. You do **NOT** need to run any database migration scripts — the database is centralized in the cloud and already configured.

**AI Provider Setup**:
Fill in `OPENAI_API_KEY` (or Azure OpenAI settings) in `.env` if you want real
AI responses from the chatbot's `/api/chatbot/ask` endpoint. Without a key it
returns a deterministic dummy response so the app still runs end-to-end.

## Run

```powershell
uvicorn app.main:app --reload --port 8000
```

## Swagger / API docs

- **Swagger UI**: http://localhost:8000/docs - interactive docs where you can
  expand any endpoint, click **Try it out**, edit the sample JSON body, and
  click **Execute** to call the live API and inspect the response/status code.
- **ReDoc**: http://localhost:8000/redoc - read-only, document-style view.
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Controllers

- `/api/welcome` - landing-page content (app name, tagline, feature list) consumed by the frontend's Welcome page
- `/api/demo` - full CRUD, used to validate the layered wiring
- `/api/employee-feedback` - sample CRUD with dummy data
- `/api/employee-skills` - sample CRUD with dummy data
- `/api/chatbot` - sample CRUD for chat history + `POST /api/chatbot/ask` for AI replies

No authentication/authorization is enabled at this stage.
