from typing import Annotated, Any
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlmodel import select

from app import crud
from app.api.dependencies import CurrentUserDep, SessionDep
from app.api.params import ExpensesQueryParams
from app.models import (
    Expense,
    ExpenseCreate,
    ExpensePublic,
    ExpenseUpdate,
    Message,
)
from app.services.expenses import (
    check_file_has_valid_headers,
    check_is_valid_csv_file,
    import_expenses_from_csv,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=list[ExpensePublic])
def get_all_expenses(
    session: SessionDep,
    current_user: CurrentUserDep,
    q: Annotated[ExpensesQueryParams, Query()],
) -> Any:
    query = select(Expense).where(Expense.user_id == current_user.id)
    if q.start_date is not None:
        query = query.where(Expense.date >= q.start_date)
    if q.finish_date is not None:
        query = query.where(Expense.date <= q.finish_date)
    if q.category is not None:
        query = query.where(Expense.category == q.category)
    query.offset(q.offset).limit(q.limit)
    tasks = session.exec(query).all()
    return tasks


@router.post("", response_model=ExpensePublic, status_code=status.HTTP_201_CREATED)
def create_new_expense(
    session: SessionDep, current_user: CurrentUserDep, expense_in: ExpenseCreate
) -> Any:
    new_expense = Expense.model_validate(expense_in)
    new_expense.user_id = current_user.id
    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)
    return new_expense


@router.get("/{expense_id}", response_model=ExpensePublic)
def get_expense_by_id(
    session: SessionDep, current_user: CurrentUserDep, expense_id: UUID
) -> Any:
    expense = crud.get_expense_by_id(session=session, expense_id=expense_id)
    if expense is None or expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    return expense


@router.patch("/{expense_id}", response_model=ExpensePublic)
def update_expense(
    session: SessionDep,
    current_user: CurrentUserDep,
    expense_id: UUID,
    expense_update: ExpenseUpdate,
):
    expense = crud.get_expense_by_id(session=session, expense_id=expense_id)
    if expense is None or expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    new_data = expense_update.model_dump(exclude_unset=True)
    new_expense = expense.sqlmodel_update(new_data)
    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)
    return new_expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    session: SessionDep, current_user: CurrentUserDep, expense_id: UUID
) -> None:
    expense = crud.get_expense_by_id(session=session, expense_id=expense_id)
    if expense is None or expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    session.delete(expense)
    session.commit()


@router.post("/import", status_code=status.HTTP_202_ACCEPTED)
async def import_expenses_from_csv_file(
    session: SessionDep,
    current_user: CurrentUserDep,
    expenses_file: UploadFile,
    background_tasks: BackgroundTasks,
) -> Message:
    try:
        check_is_valid_csv_file(expenses_file)
        contents = await expenses_file.read()
        check_file_has_valid_headers(contents)
        background_tasks.add_task(
            import_expenses_from_csv,
            session=session,
            user=current_user,
            contents=contents,
        )
        return Message(message="File accepted")
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
