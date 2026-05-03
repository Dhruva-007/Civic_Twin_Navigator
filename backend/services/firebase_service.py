import firebase_admin
from firebase_admin import credentials, firestore
from google.auth import default
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from config.settings import settings

# Setup logging
logger = logging.getLogger(__name__)


class FirebaseService:
    """
    Firebase Firestore service for Civic Twin Navigator.
    Handles all database operations using ADC credentials.
    Stores user journeys, civic twin profiles, mission progress.
    """

    def __init__(self):
        try:
            # Initialize Firebase Admin with ADC
            if not firebase_admin._apps:
                # Use ADC credentials automatically
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    "projectId": settings.firebase_project_id
                })

            # Get Firestore client
            self.db = firestore.client()
            logger.info("Firebase Firestore initialized successfully")

        except Exception as e:
            logger.error(f"Firebase initialization error: {e}")
            raise Exception(f"Firebase setup failed: {str(e)}")


    # ─────────────────────────────────────────────
    # CIVIC TWIN OPERATIONS
    # ─────────────────────────────────────────────

    def save_civic_twin(
        self,
        session_id: str,
        twin_data: Dict[str, Any]
    ) -> bool:
        """
        Save or update a Civic Twin profile.

        Args:
            session_id: Unique session identifier
            twin_data: Civic Twin profile dictionary

        Returns:
            True if saved successfully
        """
        try:
            twin_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            twin_data["session_id"] = session_id

            self.db.collection("civic_twins").document(session_id).set(
                twin_data,
                merge=True
            )
            logger.info(f"Civic Twin saved: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Save civic twin error: {e}")
            return False


    def get_civic_twin(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a Civic Twin profile by session ID.

        Args:
            session_id: Unique session identifier

        Returns:
            Civic Twin profile or None
        """
        try:
            doc = self.db.collection("civic_twins").document(session_id).get()

            if doc.exists:
                return doc.to_dict()
            else:
                logger.warning(f"Civic Twin not found: {session_id}")
                return None

        except Exception as e:
            logger.error(f"Get civic twin error: {e}")
            return None


    # ─────────────────────────────────────────────
    # JOURNEY OPERATIONS
    # ─────────────────────────────────────────────

    def save_journey(
        self,
        session_id: str,
        journey_data: Dict[str, Any]
    ) -> bool:
        """
        Save or update a user election journey.

        Args:
            session_id: Unique session identifier
            journey_data: Journey steps and metadata

        Returns:
            True if saved successfully
        """
        try:
            journey_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            journey_data["session_id"] = session_id

            self.db.collection("journeys").document(session_id).set(
                journey_data,
                merge=True
            )
            logger.info(f"Journey saved: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Save journey error: {e}")
            return False


    def get_journey(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user journey by session ID.

        Args:
            session_id: Unique session identifier

        Returns:
            Journey data or None
        """
        try:
            doc = self.db.collection("journeys").document(session_id).get()

            if doc.exists:
                return doc.to_dict()
            else:
                return None

        except Exception as e:
            logger.error(f"Get journey error: {e}")
            return None


    # ─────────────────────────────────────────────
    # MISSION OPERATIONS
    # ─────────────────────────────────────────────

    def save_mission_progress(
        self,
        session_id: str,
        mission_id: str,
        progress_data: Dict[str, Any]
    ) -> bool:
        """
        Save mission progress for a user.

        Args:
            session_id: Unique session identifier
            mission_id: Mission identifier
            progress_data: Mission progress details

        Returns:
            True if saved successfully
        """
        try:
            progress_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            progress_data["mission_id"] = mission_id
            progress_data["session_id"] = session_id

            # Save under missions/{session_id}/progress/{mission_id}
            self.db.collection("missions")\
                   .document(session_id)\
                   .collection("progress")\
                   .document(mission_id)\
                   .set(progress_data, merge=True)

            logger.info(f"Mission progress saved: {session_id}/{mission_id}")
            return True

        except Exception as e:
            logger.error(f"Save mission progress error: {e}")
            return False


    def get_mission_progress(
        self,
        session_id: str,
        mission_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get mission progress for a specific mission.

        Args:
            session_id: Unique session identifier
            mission_id: Mission identifier

        Returns:
            Mission progress or None
        """
        try:
            doc = self.db.collection("missions")\
                         .document(session_id)\
                         .collection("progress")\
                         .document(mission_id)\
                         .get()

            if doc.exists:
                return doc.to_dict()
            return None

        except Exception as e:
            logger.error(f"Get mission progress error: {e}")
            return None


    def get_all_missions_progress(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all mission progress for a user session.

        Args:
            session_id: Unique session identifier

        Returns:
            List of all mission progress records
        """
        try:
            docs = self.db.collection("missions")\
                          .document(session_id)\
                          .collection("progress")\
                          .stream()

            return [doc.to_dict() for doc in docs]

        except Exception as e:
            logger.error(f"Get all missions error: {e}")
            return []


    # ─────────────────────────────────────────────
    # READINESS SCORE OPERATIONS
    # ─────────────────────────────────────────────

    def save_readiness_score(
        self,
        session_id: str,
        score_data: Dict[str, Any]
    ) -> bool:
        """
        Save readiness score for a user.

        Args:
            session_id: Unique session identifier
            score_data: Readiness score breakdown

        Returns:
            True if saved successfully
        """
        try:
            score_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            score_data["session_id"] = session_id

            self.db.collection("readiness_scores").document(session_id).set(
                score_data,
                merge=True
            )
            logger.info(f"Readiness score saved: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Save readiness score error: {e}")
            return False


    def get_readiness_score(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get readiness score for a user.

        Args:
            session_id: Unique session identifier

        Returns:
            Readiness score or None
        """
        try:
            doc = self.db.collection("readiness_scores").document(session_id).get()

            if doc.exists:
                return doc.to_dict()
            return None

        except Exception as e:
            logger.error(f"Get readiness score error: {e}")
            return None


    # ─────────────────────────────────────────────
    # CONVERSATION HISTORY OPERATIONS
    # ─────────────────────────────────────────────

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> bool:
        """
        Save a single conversation message.

        Args:
            session_id: Unique session identifier
            role: user or model
            content: Message text

        Returns:
            True if saved successfully
        """
        try:
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": session_id
            }

            self.db.collection("conversations")\
                   .document(session_id)\
                   .collection("messages")\
                   .add(message)

            return True

        except Exception as e:
            logger.error(f"Save message error: {e}")
            return False


    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent conversation history for a session.

        Args:
            session_id: Unique session identifier
            limit: Maximum number of messages to retrieve

        Returns:
            List of messages ordered by timestamp
        """
        try:
            docs = self.db.collection("conversations")\
                          .document(session_id)\
                          .collection("messages")\
                          .order_by("timestamp")\
                          .limit_to_last(limit)\
                          .get()

            return [doc.to_dict() for doc in docs]

        except Exception as e:
            logger.error(f"Get conversation history error: {e}")
            return []


    # ─────────────────────────────────────────────
    # UTILITY OPERATIONS
    # ─────────────────────────────────────────────

    def delete_session(self, session_id: str) -> bool:
        """
        Delete all data for a session (cleanup).

        Args:
            session_id: Unique session identifier

        Returns:
            True if deleted successfully
        """
        try:
            collections = [
                "civic_twins",
                "journeys",
                "readiness_scores"
            ]

            for col in collections:
                self.db.collection(col).document(session_id).delete()

            logger.info(f"Session deleted: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Delete session error: {e}")
            return False


    def test_connection(self) -> Dict[str, Any]:
        """
        Test Firestore connection.

        Returns:
            Connection test result
        """
        try:
            # Write a test document
            test_ref = self.db.collection("health_check").document("test")
            test_ref.set({
                "status": "connected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "project": settings.firebase_project_id
            })

            # Read it back
            doc = test_ref.get()

            if doc.exists:
                # Clean up
                test_ref.delete()
                return {
                    "connected": True,
                    "project": settings.firebase_project_id,
                    "message": "Firestore read/write successful"
                }
            else:
                return {
                    "connected": False,
                    "error": "Write succeeded but read failed"
                }

        except Exception as e:
            logger.error(f"Firestore connection test error: {e}")
            return {
                "connected": False,
                "error": str(e)
            }


# Single instance to use across all agents
firebase_service = FirebaseService()