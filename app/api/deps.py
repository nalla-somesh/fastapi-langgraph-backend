from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.rate_limiter import limiter
import structlog

logger = structlog.get_logger()


async def get_database_session(db: Session = Depends(get_db)) -> Session:
    """Get database session dependency."""
    return db


def get_rate_limiter():
    """Get rate limiter dependency."""
    return limiter


async def validate_session_id(session_id: str) -> str:
    """Validate session ID format."""
    if not session_id or len(session_id) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID"
        )
    return session_id
