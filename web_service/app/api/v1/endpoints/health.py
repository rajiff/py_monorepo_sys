from typing import Any
from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import get_session

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=dict[str, Any])
async def health_check() -> dict[str, Any]:
    """
    Check the health of the application and its database connection.
    """
    try:
        async with get_session() as session:
            # Perform a simple query to verify database connection
            await session.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
