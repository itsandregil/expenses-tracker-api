import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


def get_datetime() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True)


class UserPublic(UserBase):
    id: UUID


class UserCreate(UserBase):
    password: str = Field(max_length=255)


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None


class User(UserBase, table=True):
    __tablename__: str = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = True
    joined_at: datetime.datetime = Field(default_factory=get_datetime)


class ExpenseBase(SQLModel):
    description: str = Field(max_length=255)
    amount: float = Field(gt=0)
    date: datetime.date
    category: str = Field(max_length=50)


class ExpensePublic(ExpenseBase):
    id: UUID


class ExpenseCreate(ExpenseBase): ...


class ExpenseUpdate(SQLModel):
    description: str | None = Field(default=None, max_length=255)
    amount: float | None = Field(default=None, gt=0)
    date: datetime.date | None = None
    category: str | None = Field(default=None, max_length=50)


class Expense(SQLModel, table=True):
    __tablename__: str = "expenses"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(None, foreign_key="users.id")


class TokenPayload(SQLModel):
    sub: UUID
    email: EmailStr


class Token(SQLModel):
    access_token: str
    token_type: str
