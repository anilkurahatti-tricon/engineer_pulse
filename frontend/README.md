# Frontend (React + Vite)

Layered structure:

```
frontend/
  src/
    dataservice/   # axios API clients, one per backend controller
    business/      # React hooks wrapping data-service calls (state, CRUD orchestration)
    pages/         # presentation layer (one page per controller)
    components/    # shared UI (NavBar)
    App.jsx        # routes
  .env.example
```

## Setup

```powershell
cd frontend
copy .env.example .env
npm install
```

`VITE_API_BASE_URL` in `.env` should point at the backend (default
`http://localhost:8000`).

## Run

Make sure the backend is running first (see [../backend/README.md](../backend/README.md)),
then:

```powershell
npm run dev
```

App: http://localhost:5173

Pages: Welcome (landing page), Demo, Employee Feedback, Employee Skills,
Chatbot - each calling the matching backend controller. The Welcome page
fetches its copy from `/api/welcome` and falls back to built-in placeholder
text if the backend isn't reachable yet.
