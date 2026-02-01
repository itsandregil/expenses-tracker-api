from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.dependencies import SessionDep
from app.core.config import settings
from app.core.security import create_access_token
from app.models import Token

router = APIRouter(tags=["auth"])


@router.post("/login/access-token")
def get_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = crud.authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Invalid username or password",
        )
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email},
        expires_delta,
    )
    return Token(access_token=access_token, token_type="bearer")
