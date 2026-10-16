from typing import Any
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies.session import SessionDep

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=dict[str, Any])
async def health_check(
    session: SessionDep,
) -> dict[str, Any]:
    """
    Check whether the application can execute a database query.

    The session is provided and cleaned up by the FastAPI dependency.
    This endpoint does not own the session lifecycle.
    """
    try:
        await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
        }
    except SQLAlchemyError as exc:
        # Log the exception internally with appropriate context.
        # Avoid returning database exception details to clients.
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
            },
        ) from exc
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
