from typing import Annotated, Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.core.db import engine
from app.core.security import ALGORITHM
from app.models import TokenPayload, User

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth_scheme)],
) -> User:
    try:
        payload = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Not authorized",
        )
    user = crud.get_user_by_id(session=session, id=token_data.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is inactive",
        )
    return user


SessionDep = Annotated[Session, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_active_user)]
