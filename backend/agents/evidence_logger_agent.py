from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from services.firebase_service import firebase_service
from utils.helpers import get_timestamp, generate_id

logger = logging.getLogger(__name__)


class EvidenceLoggerAgent:
    """
    Agent 10 – Evidence Logger Agent

    Responsibilities:
    - Log all sources and references for responses
    - Attach timestamps to every action
    - Track which agent provided what information
    - Store explanation of recommendations
    - Maintain audit trail for transparency
    """

    def __init__(self):
        self.log_collection = "evidence_logs"

    def log_agent_response(
        self,
        session_id: str,
        agent_name: str,
        response_data: Dict[str, Any],
        sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Log an agent's response with evidence.

        Args:
            session_id: User session ID
            agent_name: Name of the agent
            response_data: The data produced by the agent
            sources: List of sources used

        Returns:
            Log entry
        """
        try:
            log_entry = {
                "log_id": generate_id(),
                "session_id": session_id,
                "agent_name": agent_name,
                "response_summary": self._summarize_response(response_data),
                "sources": sources or ["Election Commission of India - eci.gov.in"],
                "timestamp": get_timestamp(),
                "log_type": "agent_response"
            }

            # Save to Firebase
            firebase_service.db.collection(self.log_collection).document(
                log_entry["log_id"]
            ).set(log_entry)

            logger.info(f"Log entry created: {log_entry['log_id']} for {agent_name}")

            return {
                "success": True,
                "log_entry": log_entry,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Log agent response error: {e}")
            return {"success": False, "error": str(e)}

    def log_action(
        self,
        session_id: str,
        action: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Log a user action.

        Args:
            session_id: User session ID
            action: Action performed
            details: Action details

        Returns:
            Log entry
        """
        try:
            log_entry = {
                "log_id": generate_id(),
                "session_id": session_id,
                "action": action,
                "details": details,
                "timestamp": get_timestamp(),
                "log_type": "user_action"
            }

            firebase_service.db.collection(self.log_collection).document(
                log_entry["log_id"]
            ).set(log_entry)

            return {
                "success": True,
                "log_entry": log_entry,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Log action error: {e}")
            return {"success": False, "error": str(e)}

    def log_readiness_proof(
        self,
        session_id: str,
        proof_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Log the 'Proof of Readiness' certificate.

        Args:
            session_id: User session ID
            proof_data: Readiness certificate data

        Returns:
            Log entry with certificate ID
        """
        try:
            certificate_id = proof_data.get("certificate_id", f"CERT-{session_id[:8]}")

            log_entry = {
                "log_id": certificate_id,
                "session_id": session_id,
                "proof_type": "readiness_certificate",
                "certificate_data": proof_data,
                "timestamp": get_timestamp(),
                "log_type": "readiness_proof"
            }

            firebase_service.db.collection(self.log_collection).document(
                certificate_id
            ).set(log_entry)

            return {
                "success": True,
                "certificate_id": certificate_id,
                "message": "Readiness proof logged successfully",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Log readiness proof error: {e}")
            return {"success": False, "error": str(e)}

    def get_session_logs(
        self,
        session_id: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve all logs for a session.

        Args:
            session_id: User session ID
            limit: Max logs to retrieve

        Returns:
            List of log entries
        """
        try:
            # Use new Firestore filter syntax to avoid deprecation warning
            from google.cloud.firestore_v1.base_query import FieldFilter

            docs = firebase_service.db.collection(self.log_collection)\
                .where(filter=FieldFilter("session_id", "==", session_id))\
                .limit(limit)\
                .get()

            logs = [doc.to_dict() for doc in docs]

            return {
                "success": True,
                "session_id": session_id,
                "log_count": len(logs),
                "logs": logs,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get session logs error: {e}")
            # Fallback without ordering if composite index not ready yet
            try:
                from google.cloud.firestore_v1.base_query import FieldFilter

                docs = firebase_service.db.collection(self.log_collection)\
                    .where(filter=FieldFilter("session_id", "==", session_id))\
                    .limit(limit)\
                    .get()

                logs = [doc.to_dict() for doc in docs]

                return {
                    "success": True,
                    "session_id": session_id,
                    "log_count": len(logs),
                    "logs": logs,
                    "timestamp": get_timestamp(),
                    "note": "Results without ordering - index still building"
                }

            except Exception as e2:
                logger.error(f"Fallback get session logs error: {e2}")
                return {
                    "success": False,
                    "error": str(e2),
                    "session_id": session_id
                }

    def _summarize_response(self, data: Dict[str, Any]) -> str:
        """Create a short summary of response data."""
        try:
            if isinstance(data, dict):
                keys = list(data.keys())
                return f"Response with keys: {keys[:3]}..."
            return str(data)[:100]
        except Exception:
            return "Unknown response structure"


evidence_logger_agent = EvidenceLoggerAgent()