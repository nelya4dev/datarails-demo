"""Employee schemas for CRUD operations and API responses."""

from uuid import UUID
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Create Schema (CRUD)
class EmployeeCreate(BaseModel):
    """Schema for creating a new employee.

    Includes both source data from Excel and transformed fields.
    Used internally during upload processing after transformations are applied.
    """
    # Source data (from Excel - EXACT column names)
    employee_id: str = Field(..., description="Employee ID from Excel (business key)")
    name: Optional[str] = Field(None, description="Employee full name from Excel")
    department_code: Optional[str] = Field(None, description="Department code from Excel")
    salary: Optional[float] = Field(None, description="Original salary amount from Excel")
    hire_date: Optional[date] = Field(None, description="Employee hire date from Excel")

    # Transformed data (from config.csv rules)
    department_name: Optional[str] = Field(None, description="Transformed department name")
    annual_salary_eur: Optional[float] = Field(None, description="Transformed salary in EUR")
    tenure_years: Optional[int] = Field(None, description="Calculated years of service")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "employee_id": "E0001",
                "name": "Kevin Davis",
                "department_code": "DEV",
                "salary": 78289.00,
                "hire_date": "2023-04-05",
                "department_name": "Development",
                "annual_salary_eur": 72000.00,
                "tenure_years": 1
            }
        }
    )


# Update Schema (CRUD)
class EmployeeUpdate(BaseModel):
    """Schema for updating an existing employee.

    All fields are optional to support partial updates.
    Used in UPSERT operations during upload processing.
    """
    # Source data
    name: Optional[str] = None
    department_code: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[date] = None

    # Transformed data
    department_name: Optional[str] = None
    annual_salary_eur: Optional[float] = None
    tenure_years: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Kevin Davis",
                "department_code": "DEV",
                "department_name": "Development",
                "annual_salary_eur": 75000.00,
                "tenure_years": 2
            }
        }
    )


class EmployeeInDB(BaseModel):
    """Employee data as stored in database and returned by API.

    Includes all fields from the Employee model:
    - Source data from Excel (exact column names)
    - Transformed data from config.csv
    - Internal UUID and timestamps

    Used for API responses (GET /api/employees).
    """
    # Internal fields
    id: UUID = Field(..., description="Internal UUID primary key")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    # Source data
    employee_id: str = Field(..., description="Employee ID (business key)")
    name: Optional[str] = Field(None, description="Employee full name")
    department_code: Optional[str] = Field(None, description="Department code")
    salary: Optional[float] = Field(None, description="Original salary amount")
    hire_date: Optional[date] = Field(None, description="Employee hire date")

    # Transformed data
    department_name: Optional[str] = Field(None, description="Transformed department name")
    annual_salary_eur: Optional[float] = Field(None, description="Transformed salary in EUR")
    tenure_years: Optional[int] = Field(None, description="Calculated years of service")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2025-11-17T10:00:00Z",
                "updated_at": "2025-11-17T10:00:00Z",
                "employee_id": "E0001",
                "name": "Kevin Davis",
                "department_code": "DEV",
                "salary": 78289.00,
                "hire_date": "2023-04-05",
                "department_name": "Development",
                "annual_salary_eur": 72000.00,
                "tenure_years": 1
            }
        }
    )
