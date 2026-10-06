# Frontend (React + Vite)

Layered structure:

```
frontend/
  src/
    dataservice/   # axios API clients, one per backend controller
    business/      # React hooks wrapping data-service calls (state, CRUD orchestration)
    pages/         # presentation layer (one page per controller)
    components/    # shared UI (NavBar, Recharts charts)
    theme.js       # Material UI theme
    App.jsx        # routes
  .env.example
```

UI plugins:

- `@mui/material` + `@emotion/react` + `@emotion/styled` - component library (tables, forms, ratings, alerts)
- `@mui/icons-material` - navigation and action icons
- `recharts` - rating and proficiency charts on Feedback and Skills pages
- `@fontsource/roboto` - Material UI typeface

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
Chatbot, and Gap Analysis. The Gap Analysis page is a responsive dashboard
with readiness, strength, gap-priority, and improvement-area sections. It
currently renders built-in sample data and uses the existing Recharts package.
