"""Employee API endpoints."""

import math
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.crud.employee_crud import employee_crud
from backend.schemas.employee import EmployeeInDB
from backend.schemas.common import (
    BaseResponse,
    BaseErrorResponse,
    PaginatedResponse
)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get(
    "",
    response_model=BaseResponse[PaginatedResponse[EmployeeInDB]],
    status_code=status.HTTP_200_OK,
    summary="Get employees list",
    description="""
    Get paginated list of employees with transformed data.

    Returns employees ordered by ID with optional department filtering.
    All responses are wrapped in BaseResponse structure for consistency.

    **Query parameters:**
    - `page`: Page number (1-indexed). Default: 1
    - `size`: Number of items per page. Default: 20, Max: 100
    - `department`: Optional filter by department name (e.g., "Human Resources")

    **Examples:**
    - Get all employees: `GET /api/employees`
    - Get HR employees: `GET /api/employees?department=Human%20Resources`
    - Get page 2 with 50 items: `GET /api/employees?page=2&size=50`

    **Success Response:**
    ```json
    {
      "success": true,
      "data": {
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "employee_id": "E001",
            "department_name": "Human Resources",
            "annual_salary_eur": 46000.00,
            "tenure_years": 5,
            "created_at": "2025-11-16T14:30:00Z",
            "updated_at": "2025-11-16T14:30:00Z"
          }
        ],
        "total": 100,
        "page": 1,
        "size": 20,
        "pages": 5
      }
    }
    ```

    **Empty Result (no employees found):**
    ```json
    {
      "success": true,
      "data": {
        "items": [],
        "total": 0,
        "page": 1,
        "size": 20,
        "pages": 0
      }
    }
    ```
    """,
    responses={
        200: {
            "description": "Successful response with paginated employee list",
            "model": BaseResponse[PaginatedResponse[EmployeeInDB]]
        },
        400: {
            "description": "Bad request (invalid query parameters)",
            "model": BaseErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": BaseErrorResponse
        }
    }
)
async def get_employees(
        page: int = Query(
            default=1,
            ge=1,
            description="Page number (1-indexed)",
            example=1
        ),
        size: int = Query(
            default=20,
            ge=1,
            le=100,
            description="Items per page (max 100)",
            example=20
        ),
        department: Optional[str] = Query(
            default=None,
            description="Filter by department name",
            example="Human Resources"
        ),
        db: Session = Depends(get_db)
) -> BaseResponse[PaginatedResponse[EmployeeInDB]]:
    """Get paginated list of employees with optional department filter.

    Flow:
    1. Build filters dictionary from query parameters
    2. Get employees using base CRUD method (get_multi_with_filter)
    3. Get total count using base CRUD method (count_with_filter)
    4. Convert to EmployeeInDB schemas
    5. Calculate pagination metadata
    6. Wrap in PaginatedResponse
    7. Wrap in BaseResponse for consistency

    Args:
        page: Page number (1-indexed).
        size: Number of items per page.
        department: Optional department name filter.
        db: Database session (injected by FastAPI).

    Returns:
        BaseResponse containing PaginatedResponse with employee list.
        Returns empty list if no employees found (total=0, items=[]).

    Raises:
        HTTPException 500: If database error occurs.
    """
    try:
        skip = (page - 1) * size

        filters = {}
        if department:
            filters["department_name"] = department

        employees = employee_crud.get_multi_with_filter(
            db,
            filters=filters if filters else None,
            skip=skip,
            limit=size
        )

        total = employee_crud.count_with_filter(
            db,
            filters=filters if filters else None
        )

        items = [EmployeeInDB.model_validate(emp) for emp in employees]

        pages = math.ceil(total / size) if total > 0 else 0

        paginated_data = PaginatedResponse[EmployeeInDB](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

        return BaseResponse[PaginatedResponse[EmployeeInDB]](
            success=True,
            data=paginated_data
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 404 above)
        raise

    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve employees: {str(e)}"
        )
