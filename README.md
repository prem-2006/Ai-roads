# Road Accident Intelligence System

Production-ready full-stack AI web app for road safety analytics.

## Folder Structure

```text
AI road/
  backend/
    app/
      config.py
      main.py
      db/databricks_client.py
      models/schemas.py
      services/analytics.py
      services/ai_service.py
    requirements.txt
    .env.example
  frontend/
    src/
      api/client.js
      components/
      pages/
      App.jsx
      main.jsx
      styles.css
    package.json
    .env.example
  README.md
```

## Features

- Dashboard with:
  - total accidents by state (bar chart)
  - top 5 dangerous states
  - accident trend (line chart)
- India heatmap page with high/medium/low risk highlighting
- AI chat assistant (ChatGPT-style interface)
- Databricks SQL integration with fallback mock data
- Loading states, error handling, responsive dark glassmorphism UI

## Backend Setup (FastAPI)

1. Open terminal in `backend/`.
2. Create and activate a virtual environment.
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Create `.env` from `.env.example` and set values:
   - `OPENAI_API_KEY`
   - `DATABRICKS_SERVER_HOSTNAME`
   - `DATABRICKS_HTTP_PATH`
   - `DATABRICKS_ACCESS_TOKEN`
5. Run API:
   - `uvicorn app.main:app --reload --port 8000`

API endpoints:
- `GET /api/v1/get-stats`
- `GET /api/v1/predict`
- `POST /api/v1/ask`

## Frontend Setup (React + Vite)

1. Open terminal in `frontend/`.
2. Install dependencies:
   - `npm install`
3. Create `.env` from `.env.example`:
   - `VITE_API_BASE_URL=http://localhost:8000/api/v1`
4. Start app:
   - `npm run dev`

Frontend runs on:
- `http://localhost:5173`

## Databricks Table Assumption

Delta table `accidents` with at least:
- `state` (string)
- `month` (string, e.g. `2025-01`)
- `accidents` (int)

Core query used:

```sql
SELECT state, SUM(accidents) AS accidents
FROM accidents
GROUP BY state
ORDER BY accidents DESC;
```

## AI Prompting Logic

System prompt in backend:

`You are a road safety analyst. Analyze the data and answer clearly.`

For each `/ask` request, backend:
1. fetches latest summary from analytics service
2. sends user question + summary JSON to LLM
3. returns concise, insight-focused response

## Deployment Notes

- Backend:
  - can be deployed on Render, Railway, Azure App Service, ECS, etc.
  - set environment variables from `.env.example`
- Frontend:
  - deploy via Vercel/Netlify
  - set `VITE_API_BASE_URL` to deployed backend URL
- Enable HTTPS and lock CORS origins before production launch.
