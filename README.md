# Task Management API

A backend-only Expense Tracker API for managing personal expenses.

Built to demonstrate backend fundamentals such as REST API design, authentication, SQL-based aggregation, pagination, and file ingestion using FastAPI and PostgreSQL.

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLModel**
- **Alembic**
- **Pytest**

## Features

- JWT-based authentication
- Filtering by category and date range
- Monthly reports with SQL aggregations
- Expenses imports from CSV files.

### Database Design
[![expenses_tracker_api_dark.png](https://i.postimg.cc/yxNWXzYn/expenses_tracker_api_dark.png)](https://postimg.cc/JD91MvXB)

### REST API Design
- Proper HTTP methods and status codes
- Versioned API (`/api/v1`)
- Pagination with `limit` and `offset`

## Future Improvements
- Rate limiting and caching
- Data export endpoints
- AI-based expenses analysis and recommendations
- Budgeting and recurring expenses

## Running the project

### Requirements
- [uv](https://docs.astral.sh/uv/) (package manager)
- Python 3.10+
- PostgreSQL

### Setup

```bash
git clone <repo-url>
cd expenses-tracker-api/

uv sync # Install all the packages
alembic upgrade head # Run migrations
fastapi dev # Run the API in development
```

API docs available at `http://localhost:8000/docs`.
