from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class MissionQuestion(BaseModel):
    question_id: str
    question: str
    type: str = "multiple_choice"
    options: Optional[List[str]] = []
    correct_answer: str
    explanation: str
    hint: Optional[str] = None


class MissionScenario(BaseModel):
    story: Optional[str] = None
    context: Optional[str] = None
    character: Optional[str] = None


class MissionModel(BaseModel):
    mission_id: str
    mission_number: int
    title: str
    description: Optional[str] = None
    learning_objectives: Optional[List[str]] = []
    estimated_time_minutes: Optional[int] = 10
    scenario: Optional[MissionScenario] = None
    questions: Optional[List[MissionQuestion]] = []
    key_takeaways: Optional[List[str]] = []
    completion_message: Optional[str] = None
    next_mission_preview: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class MissionProgress(BaseModel):
    session_id: str
    mission_id: str
    status: str = "started"
    mission_number: Optional[int] = None
    total_questions: Optional[int] = 0
    answered_questions: Optional[int] = 0
    score: Optional[int] = 0
    last_answered: Optional[str] = None
    updated_at: Optional[str] = None