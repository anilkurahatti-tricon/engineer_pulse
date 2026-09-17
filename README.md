# Engineer Pulse

APEX program project for Batch 4 and squad 4.

Engineer Pulse is a full-stack application with a React front end and a
Python/FastAPI back end, structured in layers (controllers -> business ->
dataservice) so it can grow into AI-powered features (chatbot, insights)
over time. No authentication/authorization is implemented yet.

## Tech stack

- Frontend: React (Vite), Material UI, MUI Icons, Recharts
- Backend: Python, FastAPI, Swagger/OpenAPI docs enabled at `/docs`
- Data: in-memory dummy stores for now, isolated behind a `dataservice` layer
  so a real database can be swapped in later without touching business logic
- AI: pluggable client (OpenAI / Azure OpenAI) configured via `.env`

## Project structure

```
engineer_pulse/
├── backend/                          # FastAPI, Python
│   ├── app/
│   │   ├── controllers/              # API layer: demo, employee_feedback, employee_skills, chatbot
│   │   ├── business/                 # service layer (one service per controller)
│   │   ├── dataservice/              # in-memory "repositories" with seeded dummy data
│   │   ├── models/                   # Pydantic schemas
│   │   ├── ai/ai_client.py           # pluggable OpenAI/Azure OpenAI client, extracts keys from .env
│   │   ├── core/config.py            # Settings (reads .env)
│   │   └── main.py                   # app entrypoint, Swagger at /docs, CORS open
│   ├── requirements.txt              # fastapi, uvicorn, pydantic-settings, openai, tiktoken, pytest, httpx
│   ├── .env.example
│   └── README.md
├── frontend/                         # React (Vite)
│   └── src/
│       ├── dataservice/              # axios clients per controller
│       ├── business/                 # hooks wrapping data-service + state
│       ├── pages/                    # DemoPage, EmployeeFeedbackPage, EmployeeSkillsPage, ChatbotPage
│       ├── components/               # NavBar, Recharts visualizations
│       └── theme.js                  # Material UI theme
├── .gitignore                        # merged Python + Node + .env rules
└── README.md
```

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md)
for setup and run instructions for each part.

## Controllers

| Controller | Path | Notes |
|---|---|---|
| Welcome | `/api/welcome` | Landing-page content shown on the frontend's home screen |
| Demo | `/api/demo` | Full CRUD used to validate the layered setup |
| Employee Feedback | `/api/employee-feedback` | Sample CRUD with dummy data |
| Employee Skills | `/api/employee-skills` | Sample CRUD with dummy data |
| Chatbot | `/api/chatbot` | Sample CRUD for chat history + `POST /ask` for AI replies |

## How to run this application

You need two terminals: one for the backend (FastAPI) and one for the
frontend (React/Vite). Both must be running at the same time.

### 1. Start the backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

The API is now available at http://localhost:8000. Leave this terminal running.

### 2. Start the frontend

Open a **new** terminal:

```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```

Open http://localhost:5173 in your browser - you'll land on the Welcome page,
with links to Demo, Employee Feedback, Employee Skills, and Chatbot.

## Swagger / API docs

The backend exposes interactive API documentation as soon as it's running:

- **Swagger UI**: http://localhost:8000/docs - browse every endpoint, expand
  a route, click **Try it out**, fill in sample values, and click **Execute**
  to call the real API and see the response, right from the browser.
- **ReDoc**: http://localhost:8000/redoc - a read-only, more document-style
  view of the same API.
- **Raw OpenAPI schema**: http://localhost:8000/openapi.json

No login is required to use Swagger since authentication is not enabled yet.
