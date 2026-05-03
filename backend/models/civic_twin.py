from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional, List


class PersonalInfo(BaseModel):
    """Personal information extracted from user input."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    location: Optional[str] = None
    state: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    residence_type: Optional[str] = None


class VoterProfile(BaseModel):
    """Voter registration and eligibility profile."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    voter_status: Optional[str] = None
    is_eligible: Optional[bool] = None
    registration_status: Optional[str] = None
    has_voter_id: Optional[bool] = None
    constituency: Optional[str] = None


class DocumentStatus(BaseModel):
    """Status of documents required for voter registration."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    has_aadhar: Optional[bool] = None
    has_address_proof: Optional[bool] = None
    has_age_proof: Optional[bool] = None
    document_concerns: Optional[List[str]] = []


class AccessibilityProfile(BaseModel):
    """Accessibility preferences and requirements."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    language_preference: Optional[str] = "en"
    literacy_level: Optional[str] = "intermediate"
    needs_voice_support: Optional[bool] = False
    needs_simple_language: Optional[bool] = False
    special_needs: Optional[str] = None


class CivicTwinModel(BaseModel):
    """
    Complete Civic Twin profile model.

    Represents a user's personalized voter profile
    including personal info, voter status, documents,
    accessibility needs, and risk factors.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: str
    personal_info: Optional[PersonalInfo] = None
    voter_profile: Optional[VoterProfile] = None
    document_status: Optional[DocumentStatus] = None
    accessibility_profile: Optional[AccessibilityProfile] = None
    risk_factors: Optional[List[str]] = []
    priority_concerns: Optional[List[str]] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    profile_completeness: Optional[int] = 0


class CivicTwinCreateRequest(BaseModel):
    """Request model for creating a Civic Twin."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_input: str
    language: Optional[str] = "en"


class CivicTwinQueryRequest(BaseModel):
    """Request model for querying election information."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: Optional[str] = None
    query: str
    language: Optional[str] = "en"


class CivicTwinUpdateRequest(BaseModel):
    """Request model for updating a Civic Twin profile."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: str
    new_input: str