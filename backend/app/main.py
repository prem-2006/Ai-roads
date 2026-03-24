from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models.schemas import AskRequest, AskResponse, PredictResponse, StatsResponse
from app.services.ai_service import AIService
from app.services.analytics import AnalyticsService

settings = get_settings()
analytics_service = AnalyticsService()
ai_service = AIService()

app = FastAPI(title="Road Accident Intelligence System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": "Road Accident Intelligence System"}


@app.get(f"{settings.api_v1_prefix}/get-stats", response_model=StatsResponse)
def get_stats():
    try:
        return analytics_service.get_stats()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {exc}") from exc


@app.get(f"{settings.api_v1_prefix}/predict", response_model=PredictResponse)
def predict():
    try:
        data = analytics_service.predict_risk()
        return {"risk_map": data["risk_map"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


@app.post(f"{settings.api_v1_prefix}/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    try:
        stats = analytics_service.get_stats()
        answer = ai_service.ask(payload.question, stats)
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI assistant failed: {exc}") from exc
