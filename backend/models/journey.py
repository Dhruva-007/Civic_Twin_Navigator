from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class JourneyStep(BaseModel):
    step_id: str
    title: str
    description: Optional[str] = None
    action: Optional[str] = None
    is_completed: bool = False
    is_required: bool = True
    resources: Optional[List[str]] = []
    completed_at: Optional[str] = None


class JourneyPhase(BaseModel):
    phase_id: str
    phase_number: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    estimated_days: Optional[int] = None
    steps: Optional[List[JourneyStep]] = []


class JourneyModel(BaseModel):
    session_id: str
    journey_title: Optional[str] = None
    total_phases: Optional[int] = 0
    estimated_completion_days: Optional[int] = 30
    phases: Optional[List[JourneyPhase]] = []
    personalization_notes: Optional[List[str]] = []
    important_reminders: Optional[List[str]] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True