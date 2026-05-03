import firebase_admin
from firebase_admin import auth
from typing import Dict, Any, Optional
import logging

from utils.helpers import get_timestamp

logger = logging.getLogger(__name__)


class AuthService:
    """
    Firebase Authentication service for Civic Twin Navigator.
    Verifies Firebase ID tokens and manages user profiles.
    Uses existing Firebase Admin SDK initialized in firebase_service.
    """

    def verify_token(self, id_token: str) -> Dict[str, Any]:
        """
        Verify a Firebase ID token from the frontend.

        Args:
            id_token: Firebase ID token string from frontend

        Returns:
            Decoded token data with user info
        """
        try:
            decoded_token = auth.verify_id_token(id_token)

            return {
                "success": True,
                "user_id": decoded_token.get("uid"),
                "email": decoded_token.get("email"),
                "name": decoded_token.get("name"),
                "picture": decoded_token.get("picture"),
                "email_verified": decoded_token.get("email_verified", False),
                "sign_in_provider": decoded_token.get(
                    "firebase", {}
                ).get("sign_in_provider", "unknown"),
                "timestamp": get_timestamp()
            }

        except auth.ExpiredIdTokenError:
            logger.warning("Expired Firebase token received")
            return {
                "success": False,
                "error": "Token expired. Please sign in again."
            }
        except auth.InvalidIdTokenError:
            logger.warning("Invalid Firebase token received")
            return {
                "success": False,
                "error": "Invalid token. Please sign in again."
            }
        except auth.RevokedIdTokenError:
            logger.warning("Revoked Firebase token received")
            return {
                "success": False,
                "error": "Session revoked. Please sign in again."
            }
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return {
                "success": False,
                "error": "Authentication failed. Please try again."
            }

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get Firebase user record by user ID.

        Args:
            user_id: Firebase user UID

        Returns:
            User record data
        """
        try:
            user_record = auth.get_user(user_id)

            return {
                "success": True,
                "user_id": user_record.uid,
                "email": user_record.email,
                "name": user_record.display_name,
                "picture": user_record.photo_url,
                "email_verified": user_record.email_verified,
                "created_at": user_record.user_metadata.creation_timestamp,
                "last_sign_in": user_record.user_metadata.last_sign_in_timestamp,
                "disabled": user_record.disabled,
            }

        except auth.UserNotFoundError:
            return {
                "success": False,
                "error": "User not found"
            }
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """
        Delete a Firebase user account.

        Args:
            user_id: Firebase user UID

        Returns:
            Deletion result
        """
        try:
            auth.delete_user(user_id)
            logger.info(f"User deleted: {user_id}")
            return {"success": True, "message": "User deleted successfully"}

        except Exception as e:
            logger.error(f"Delete user error: {e}")
            return {"success": False, "error": str(e)}


# Single instance
auth_service = AuthService()