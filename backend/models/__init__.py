"""
Civic Twin Navigator - Models Package

Contains Pydantic data models for request/response validation:
- CivicTwinModel: Complete voter profile
- PersonalInfo: Personal information submodel
- VoterProfile: Voter registration status
- DocumentStatus: Document availability
- AccessibilityProfile: Accessibility preferences
- JourneyModel: Election journey structure
- JourneyPhase: Individual journey phase
- JourneyStep: Individual step in a phase
- MissionModel: Interactive mission structure
- MissionQuestion: Quiz question model
- ReadinessScoreModel: Readiness assessment
"""

from models.civic_twin import (
    CivicTwinModel,
    PersonalInfo,
    VoterProfile,
    DocumentStatus,
    AccessibilityProfile,
    CivicTwinCreateRequest,
    CivicTwinQueryRequest,
    CivicTwinUpdateRequest,
)
from models.journey import JourneyModel, JourneyPhase, JourneyStep
from models.mission import MissionModel, MissionQuestion, MissionProgress
from models.readiness_score import ReadinessScoreModel, ScoreCategory

__all__ = [
    "CivicTwinModel",
    "PersonalInfo",
    "VoterProfile",
    "DocumentStatus",
    "AccessibilityProfile",
    "CivicTwinCreateRequest",
    "CivicTwinQueryRequest",
    "CivicTwinUpdateRequest",
    "JourneyModel",
    "JourneyPhase",
    "JourneyStep",
    "MissionModel",
    "MissionQuestion",
    "MissionProgress",
    "ReadinessScoreModel",
    "ScoreCategory",
]