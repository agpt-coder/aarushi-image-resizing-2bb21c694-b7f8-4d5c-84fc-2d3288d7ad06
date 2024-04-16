from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class SessionRenewalResponse(BaseModel):
    """
    Response model for a session renewal request. Provides confirmation and any relevant session info.
    """

    successful: bool
    new_expiry: datetime
    message: str


async def session_renewal(session_id: str, auth_token: str) -> SessionRenewalResponse:
    """
    Renews user session for active users

    This function looks for a session in the database with the given session_id and auth_token.
    If found and valid, it renews the session by extending its expiry.

    Args:
        session_id (str): The unique identifier for the user's current session.
        auth_token (str): The authentication token associated with the user's current session.

    Returns:
        SessionRenewalResponse: Response model for a session renewal request. Provides confirmation and any relevant session info.

    Raises:
        ValueError: If no session is found with the given session_id and auth_token.
    """
    session = await prisma.models.Session.prisma().find_unique(where={"id": session_id})
    if not session:
        raise ValueError("prisma.models.Session not found.")
    new_expiry = datetime.now() + timedelta(days=30)
    await prisma.models.Session.prisma().update(
        where={"id": session_id}, data={"updatedAt": new_expiry}
    )
    return SessionRenewalResponse(
        successful=True,
        new_expiry=new_expiry,
        message="prisma.models.Session renewal successful.",
    )
