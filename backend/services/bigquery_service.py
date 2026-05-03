"""
BigQuery Analytics Service for Civic Twin Navigator.

Logs user events and analytics data to Google BigQuery.
Enables tracking of:
- User engagement patterns
- Mission completion rates
- Readiness score trends
- Language usage analytics
- Geographic distribution
"""

from google.cloud import bigquery
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import logging
import uuid

from config.settings import settings

logger = logging.getLogger(__name__)


class BigQueryService:
    """
    Google BigQuery analytics service.

    Logs all significant user events to BigQuery for
    analytics, reporting, and insights generation.
    """

    # BigQuery configuration
    DATASET_ID = "civic_twin_analytics"
    TABLE_ID = "user_events"

    def __init__(self):
        try:
            self.client = bigquery.Client(
                project=settings.google_cloud_project_id
            )
            self.table_ref = (
                f"{settings.google_cloud_project_id}"
                f".{self.DATASET_ID}"
                f".{self.TABLE_ID}"
            )
            logger.info(
                f"BigQuery Service initialized: {self.table_ref}"
            )
        except Exception as e:
            logger.error(f"BigQuery initialization error: {e}")
            raise Exception(f"BigQuery setup failed: {str(e)}")

    def log_event(
        self,
        event_type: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        location: Optional[str] = None,
        language: Optional[str] = None,
        voter_status: Optional[str] = None,
        readiness_score: Optional[int] = None,
        mission_number: Optional[int] = None,
        metadata: Optional[str] = None,
    ) -> bool:
        """
        Log a single user event to BigQuery.

        Args:
            event_type: Type of event (civic_twin_created, mission_completed, etc.)
            session_id: User session identifier
            user_id: Firebase user ID if authenticated
            location: User's location (city/state)
            language: Language preference code
            voter_status: first_time, registered, unsure
            readiness_score: Overall readiness score 0-100
            mission_number: Mission number if applicable
            metadata: Additional JSON string metadata

        Returns:
            True if logged successfully
        """
        try:
            row = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "session_id": session_id,
                "user_id": user_id,
                "location": location,
                "language": language,
                "voter_status": voter_status,
                "readiness_score": readiness_score,
                "mission_number": mission_number,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata,
            }

            errors = self.client.insert_rows_json(
                self.table_ref,
                [row]
            )

            if errors:
                logger.warning(f"BigQuery insert warnings: {errors}")
                return False

            logger.info(
                f"BigQuery event logged: {event_type} "
                f"session={session_id}"
            )
            return True

        except Exception as e:
            # Non-critical - log warning but don't break app flow
            logger.warning(f"BigQuery log event error (non-critical): {e}")
            return False

    def log_civic_twin_created(
        self,
        session_id: str,
        location: Optional[str] = None,
        language: Optional[str] = None,
        voter_status: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a new Civic Twin profile is created.

        Args:
            session_id: Session identifier
            location: User location
            language: Language preference
            voter_status: Voter registration status
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        return self.log_event(
            event_type="civic_twin_created",
            session_id=session_id,
            user_id=user_id,
            location=location,
            language=language,
            voter_status=voter_status,
        )

    def log_journey_created(
        self,
        session_id: str,
        location: Optional[str] = None,
        voter_status: Optional[str] = None,
        total_phases: Optional[int] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a personalized journey is created.

        Args:
            session_id: Session identifier
            location: User location
            voter_status: Voter registration status
            total_phases: Number of phases in journey
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        import json
        metadata = json.dumps({"total_phases": total_phases}) if total_phases else None

        return self.log_event(
            event_type="journey_created",
            session_id=session_id,
            user_id=user_id,
            location=location,
            voter_status=voter_status,
            metadata=metadata,
        )

    def log_mission_completed(
        self,
        session_id: str,
        mission_number: int,
        score: Optional[int] = None,
        correct_answers: Optional[int] = None,
        total_questions: Optional[int] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a user completes an interactive mission.

        Args:
            session_id: Session identifier
            mission_number: Mission number 1-5
            score: Score achieved in mission
            correct_answers: Number of correct answers
            total_questions: Total questions in mission
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        import json
        metadata = json.dumps({
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
        }) if score is not None else None

        return self.log_event(
            event_type="mission_completed",
            session_id=session_id,
            user_id=user_id,
            mission_number=mission_number,
            metadata=metadata,
        )

    def log_readiness_assessed(
        self,
        session_id: str,
        overall_score: int,
        location: Optional[str] = None,
        voter_status: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a readiness score is calculated.

        Args:
            session_id: Session identifier
            overall_score: Overall readiness score 0-100
            location: User location
            voter_status: Voter registration status
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        return self.log_event(
            event_type="readiness_assessed",
            session_id=session_id,
            user_id=user_id,
            location=location,
            voter_status=voter_status,
            readiness_score=overall_score,
        )

    def log_language_selected(
        self,
        session_id: str,
        language: str,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a user selects a language.

        Args:
            session_id: Session identifier
            language: Selected language code
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        return self.log_event(
            event_type="language_selected",
            session_id=session_id,
            user_id=user_id,
            language=language,
        )

    def log_scenario_run(
        self,
        session_id: str,
        scenario_type: Optional[str] = None,
        is_recoverable: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a what-if scenario is simulated.

        Args:
            session_id: Session identifier
            scenario_type: Type of scenario
            is_recoverable: Whether scenario is recoverable
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        import json
        metadata = json.dumps({
            "scenario_type": scenario_type,
            "is_recoverable": is_recoverable,
        }) if scenario_type else None

        return self.log_event(
            event_type="scenario_run",
            session_id=session_id,
            user_id=user_id,
            metadata=metadata,
        )

    def log_proof_generated(
        self,
        session_id: str,
        certificate_id: Optional[str] = None,
        confidence_level: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Log when a Proof of Readiness is generated.

        Args:
            session_id: Session identifier
            certificate_id: Certificate identifier
            confidence_level: Confidence level of readiness
            user_id: Firebase user ID if authenticated

        Returns:
            True if logged successfully
        """
        import json
        metadata = json.dumps({
            "certificate_id": certificate_id,
            "confidence_level": confidence_level,
        }) if certificate_id else None

        return self.log_event(
            event_type="proof_generated",
            session_id=session_id,
            user_id=user_id,
            metadata=metadata,
        )

    def log_user_login(
        self,
        user_id: str,
        sign_in_provider: Optional[str] = None,
        is_new_user: Optional[bool] = None,
    ) -> bool:
        """
        Log when a user logs in.

        Args:
            user_id: Firebase user ID
            sign_in_provider: google.com or password
            is_new_user: Whether this is first login

        Returns:
            True if logged successfully
        """
        import json
        metadata = json.dumps({
            "sign_in_provider": sign_in_provider,
            "is_new_user": is_new_user,
        })

        return self.log_event(
            event_type="user_login",
            user_id=user_id,
            metadata=metadata,
        )

    def get_analytics_summary(self) -> Dict[str, Any]:
        """
        Get high-level analytics summary from BigQuery.

        Returns:
            Analytics summary dictionary
        """
        try:
            query = f"""
                SELECT
                    event_type,
                    COUNT(*) as count,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    COUNT(DISTINCT user_id) as unique_users
                FROM `{self.table_ref}`
                WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                GROUP BY event_type
                ORDER BY count DESC
            """

            query_job = self.client.query(query)
            results = list(query_job.result())

            summary = []
            for row in results:
                summary.append({
                    "event_type": row["event_type"],
                    "count": row["count"],
                    "unique_sessions": row["unique_sessions"],
                    "unique_users": row["unique_users"],
                })

            return {
                "success": True,
                "period": "last_7_days",
                "events": summary,
            }

        except Exception as e:
            logger.warning(f"BigQuery analytics query error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_language_distribution(self) -> Dict[str, Any]:
        """
        Get language usage distribution.

        Returns:
            Language usage statistics
        """
        try:
            query = f"""
                SELECT
                    language,
                    COUNT(*) as usage_count
                FROM `{self.table_ref}`
                WHERE language IS NOT NULL
                AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
                GROUP BY language
                ORDER BY usage_count DESC
            """

            query_job = self.client.query(query)
            results = list(query_job.result())

            languages = [
                {"language": row["language"], "count": row["usage_count"]}
                for row in results
            ]

            return {
                "success": True,
                "languages": languages,
            }

        except Exception as e:
            logger.warning(f"BigQuery language query error: {e}")
            return {"success": False, "error": str(e)}

    def test_connection(self) -> Dict[str, Any]:
        """
        Test BigQuery connection by checking table exists.

        Returns:
            Connection test result
        """
        try:
            table = self.client.get_table(self.table_ref)
            return {
                "connected": True,
                "table": self.table_ref,
                "rows": table.num_rows,
                "schema_fields": len(table.schema),
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }


# Single instance
bigquery_service = BigQueryService()