"""Upload job schemas for CRUD operations and API responses."""

from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# Create Schema (internal - for CRUD operations)
class UploadJobCreate(BaseModel):
    """Schema for creating a new upload job.

    Used when initiating a new file upload. Only filename and file_path are
    required initially. Status defaults to "pending" in the model.
    """
    filename: str = Field(..., description="Original filename of uploaded file")
    file_path: str = Field(..., description="Server path where file is stored")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "employees_data.xlsx",
                "file_path": "/tmp/uploads/550e8400-e29b-41d4-a716-446655440000.xlsx"
            }
        }
    )


# Update Schema (internal - for CRUD operations)
class UploadJobUpdate(BaseModel):
    """Schema for updating an upload job.

    All fields are optional to support partial updates during processing.
    Used by Celery worker to update job status, progress, and errors.
    """
    status: Optional[str] = Field(None, description="Job status (pending/processing/completed/failed)")
    current_step: Optional[str] = Field(None, description="Current processing step")
    total_rows: Optional[int] = Field(None, ge=0, description="Total number of rows")
    processed_rows: Optional[int] = Field(None, ge=0, description="Number of rows processed")
    error_rows: Optional[int] = Field(None, ge=0, description="Number of rows with errors")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Detailed error information")
    error_message: Optional[str] = Field(None, description="Overall error message")
    started_at: Optional[datetime] = Field(None, description="When processing started")
    completed_at: Optional[datetime] = Field(None, description="When processing completed")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "status": "processing",
                "current_step": "transforming",
                "total_rows": 100,
                "processed_rows": 50,
                "error_rows": 2
            }
        }
    )


class UploadJobInDB(BaseModel):
    """Upload job data as stored in database and returned by API.

    Complete representation of an upload job including all tracking fields.
    Used for API responses.
    """
    id: UUID = Field(..., description="Internal UUID primary key")
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="Server file path")
    status: str = Field(..., description="Job status (pending/processing/completed/failed)")
    current_step: Optional[str] = Field(None, description="Current processing step")
    total_rows: Optional[int] = Field(None, description="Total number of rows")
    processed_rows: Optional[int] = Field(None, description="Number of rows processed")
    error_rows: Optional[int] = Field(None, description="Number of rows with errors")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Detailed error information")
    error_message: Optional[str] = Field(None, description="Overall error message if failed")
    started_at: Optional[datetime] = Field(None, description="When processing started")
    completed_at: Optional[datetime] = Field(None, description="When processing completed")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "filename": "employees_data.xlsx",
                "file_path": "/tmp/uploads/550e8400-e29b-41d4-a716-446655440000.xlsx",
                "status": "completed",
                "current_step": "persisting",
                "total_rows": 100,
                "processed_rows": 98,
                "error_rows": 2,
                "error_details": {
                    "errors": [
                        {"row": 5, "field": "salary", "message": "Invalid number format"},
                        {"row": 12, "field": "department", "message": "Unknown department code"}
                    ]
                },
                "error_message": None,
                "started_at": "2025-11-17T14:30:00Z",
                "completed_at": "2025-11-17T14:30:45Z",
                "created_at": "2025-11-17T14:29:55Z",
                "updated_at": "2025-11-17T14:30:45Z"
            }
        }
    )


class UploadJobResponse(BaseModel):
    """Simple response for successful file upload (POST /api/upload).

    Returns minimal information - just job_id and message.
    Client uses job_id to poll status via GET /api/upload/status/{job_id}.
    """
    job_id: str = Field(..., description="UUID of created upload job")
    message: str = Field(..., description="Success message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "File uploaded successfully. Processing started."
            }
        }
    )
