from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUserDep, SessionDep
from app.api.params import MonthlyReportQueryParams
from app.models import MonthlyReport
from app.services.expenses import get_monthly_expenses_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly")
def get_monthly_report(
    session: SessionDep,
    current_user: CurrentUserDep,
    q: Annotated[MonthlyReportQueryParams, Query()],
) -> MonthlyReport:
    monthly_report = get_monthly_expenses_report(
        session=session,
        user=current_user,
        year=q.year,
        month=q.month,
    )
    return monthly_report
