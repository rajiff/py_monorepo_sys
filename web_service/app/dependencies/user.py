from typing import Annotated
from fastapi import Depends

from app.dependencies.session import SessionDep
from app.repositories.user import UserRepository
from app.services.user import UserService

# User Repository
def get_user_repository(
    session: SessionDep,
) -> UserRepository:
    """Construct a repository using the current request's session."""
    return UserRepository(session)

UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
]

# User Service
def get_user_service(
    repository: UserRepositoryDep,
) -> UserService:
    """Construct the user service with its required repository."""
    return UserService(repository)

UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]
