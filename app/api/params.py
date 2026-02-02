from datetime import date

from sqlmodel import Field, SQLModel

from app.utils import get_current_month, get_current_year


class ExpensesQueryParams(SQLModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, gt=0, le=100)
    start_date: date | None = None
    finish_date: date | None = None
    category: str | None = None


class MonthlyReportQueryParams(SQLModel):
    year: int = Field(default_factory=get_current_year, ge=1, le=9999)
    month: int = Field(default_factory=get_current_month, ge=1, le=12)
