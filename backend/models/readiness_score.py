from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ScoreCategory(BaseModel):
    score: int = 0
    explanation: Optional[str] = None
    max_score: int = 100
    status: Optional[str] = None


class ReadinessScoreModel(BaseModel):
    session_id: str
    overall_score: int = 0
    overall_status: Optional[str] = None
    scores: Optional[Dict[str, ScoreCategory]] = {}
    key_improvement_areas: Optional[List[str]] = []
    quick_wins: Optional[List[str]] = []
    improvement_tips: Optional[List[str]] = []
    generated_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True