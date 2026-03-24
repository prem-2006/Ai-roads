from typing import Dict, List

from pydantic import BaseModel


class StateAccidentStat(BaseModel):
    state: str
    accidents: int


class StatsResponse(BaseModel):
    totals_by_state: List[StateAccidentStat]
    top_5_dangerous_states: List[StateAccidentStat]
    trend: List[Dict[str, int]]
    total_accidents: int


class PredictResponse(BaseModel):
    risk_map: List[Dict[str, str]]


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
