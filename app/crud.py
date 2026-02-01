from uuid import UUID

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Expense, User, UserCreate


def get_user_by_id(*, session: Session, id: UUID) -> User | None:
    user = session.get(User, id)
    return user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    query = select(User).where(User.email == email)
    user = session.exec(query).first()
    return user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def create_new_user(*, session: Session, user_create: UserCreate) -> User:
    new_user = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_expense_by_id(*, session: Session, expense_id: UUID) -> Expense | None:
    expense = session.get(Expense, expense_id)
    return expense
