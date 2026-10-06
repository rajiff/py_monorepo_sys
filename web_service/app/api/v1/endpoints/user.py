from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def current_user()  -> dict[str, str]:
    """Return currently logged in user profile information"""
    return {"username": "current user"}
