from typing import Any

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.dependencies import SessionDep
from app.models import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
def create_new_user(session: SessionDep, user_in: UserCreate) -> Any:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    new_user = crud.create_new_user(session=session, user_create=user_in)
    return new_user
