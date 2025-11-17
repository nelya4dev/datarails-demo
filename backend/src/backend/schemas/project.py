"""Project schemas for CRUD operations and API responses."""

from uuid import UUID
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Create Schema (CRUD)
class ProjectCreate(BaseModel):
    """Schema for creating a new project.

    Includes source data from Excel.
    Used internally during upload processing.
    """
    project_id: str = Field(..., description="Project ID from Excel (business key)")
    project_name: Optional[str] = Field(None, description="Project name from Excel")
    budget_usd: Optional[float] = Field(None, description="Budget amount in USD from Excel")
    start_date: Optional[date] = Field(None, description="Project start date from Excel")
    status: Optional[str] = Field(None, description="Project status from Excel")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "project_id": "P001",
                "project_name": "Next-Gen Platform Phase 2",
                "budget_usd": 83158.0,
                "start_date": "2024-02-17",
                "status": "Active"
            }
        }
    )


# Update Schema (CRUD)
class ProjectUpdate(BaseModel):
    """Schema for updating an existing project.

    All fields are optional to support partial updates.
    Used in UPSERT operations during upload processing.
    """
    project_name: Optional[str] = None
    budget_usd: Optional[float] = None
    start_date: Optional[date] = None
    status: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "project_name": "Next-Gen Platform Phase 3",
                "budget_usd": 90000.0,
                "status": "Complete"
            }
        }
    )


class ProjectInDB(BaseModel):
    """Project data as stored in database and returned by API.

    Includes all fields from the Project model:
    - Source data from Excel (exact column names)
    - Internal UUID and timestamps

    Used for API responses (GET /api/projects).
    """
    # Internal fields
    id: UUID = Field(..., description="Internal UUID primary key")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    # Source data (from Excel - EXACT column names)
    project_id: str = Field(..., description="Project ID (business key)")
    project_name: Optional[str] = Field(None, description="Project name")
    budget_usd: Optional[float] = Field(None, description="Budget amount in USD")
    start_date: Optional[date] = Field(None, description="Project start date")
    status: Optional[str] = Field(None, description="Project status")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2025-11-17T10:00:00Z",
                "updated_at": "2025-11-17T10:00:00Z",
                "project_id": "P001",
                "project_name": "Next-Gen Platform Phase 2",
                "budget_usd": 83158.0,
                "start_date": "2024-02-17",
                "status": "Active"
            }
        }
    )