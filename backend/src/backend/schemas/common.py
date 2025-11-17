"""Common schemas for API responses following OOP/SOLID principles."""

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Generic, TypeVar, Optional
from datetime import datetime

from backend.core.utils import utcnow

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    """Base success response wrapper for all API endpoints.

    Provides consistent response structure across the API.
    Generic type T represents the data payload type.

    Attributes:
        success: Always True for success responses.
        data: The actual response data (type T).

    Usage:
        BaseResponse[EmployeeInDB](success=True, data=employee)
        BaseResponse[PaginatedResponse[EmployeeInDB]](success=True, data=paginated_data)
    """
    success: bool = Field(default=True, description="Request success indicator")
    data: T = Field(..., description="Response payload")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": {"example": "data"}
            }
        }
    )


class BaseErrorResponse(BaseModel):
    """Base error response wrapper for all API error responses.

    Provides consistent error structure across the API.

    Attributes:
        success: Always False for error responses.
        error: Error details (ErrorDetail object).

    Usage:
        BaseErrorResponse(
            success=False,
            error=ErrorDetail(detail="Not found", error_code="NOT_FOUND")
        )
    """
    success: bool = Field(default=False, description="Request success indicator")
    error: "ErrorDetail" = Field(..., description="Error details")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": {
                    "detail": "An error occurred",
                    "error_code": "ERROR"
                }
            }
        }
    )


class ErrorDetail(BaseModel):
    """Base error detail structure.

    Contains human-readable message and machine-readable error code.
    Used in all error responses.

    Attributes:
        detail: Human-readable error message for display.
        error_code: Machine-readable error code for programmatic handling.
    """
    detail: str = Field(..., description="Human-readable error message")
    error_code: str = Field(..., description="Machine-readable error code")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Resource not found",
                "error_code": "NOT_FOUND"
            }
        }
    )


class ValidationErrorItem(BaseModel):
    """Single field validation error.

    Represents a validation failure for a specific field.
    Used in 422 Unprocessable Entity responses.

    Attributes:
        loc: Location path of the error (e.g., ["body", "email"]).
        msg: Error message describing the validation failure.
        type: Error type identifier (e.g., "value_error.email").
    """
    loc: List[str] = Field(..., description="Error location path")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type identifier")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "loc": ["body", "email"],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        }
    )


class ValidationErrorDetail(BaseModel):
    """Validation error detail for 422 responses.

    Contains list of field-level validation errors.
    Extends ErrorDetail pattern for validation-specific errors.

    Attributes:
        detail: List of validation errors.
        error_code: Always "VALIDATION_ERROR".
    """
    detail: List[ValidationErrorItem] = Field(..., description="List of validation errors")
    error_code: str = Field(default="VALIDATION_ERROR", description="Error code")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email"
                    }
                ],
                "error_code": "VALIDATION_ERROR"
            }
        }
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response for list endpoints.

    Wraps list of items with pagination metadata.
    Generic type T represents the item type.

    Attributes:
        items: List of items for current page.
        total: Total number of items across all pages.
        page: Current page number (1-indexed).
        size: Number of items per page.
        pages: Total number of pages.

    Usage:
        PaginatedResponse[EmployeeInDB](
            items=[...],
            total=100,
            page=1,
            size=20,
            pages=5
        )
    """
    items: List[T] = Field(..., description="List of items for current page")
    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number (1-indexed)")
    size: int = Field(..., ge=1, le=100, description="Items per page")
    pages: int = Field(..., ge=0, description="Total number of pages")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "size": 20,
                "pages": 5
            }
        }
    )


class PaginationParams(BaseModel):
    """Query parameters for pagination.

    Use as FastAPI dependency to parse pagination query parameters.
    Provides computed properties for database queries.

    Attributes:
        page: Page number (1-indexed).
        size: Items per page (max 100).

    Computed Properties:
        skip: Database offset for SQLAlchemy.
        limit: Database limit for SQLAlchemy.

    Usage:
        @app.get("/items")
        def get_items(pagination: PaginationParams = Depends()):
            items = crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)
    """
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    size: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")

    @property
    def skip(self) -> int:
        """Calculate database offset from page and size.

        Returns:
            Number of records to skip (offset).
        """
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        """Get database limit (same as size).

        Returns:
            Maximum number of records to return.
        """
        return self.size

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page": 1,
                "size": 20
            }
        }
    )


class MessageResponse(BaseModel):
    """Simple message response for operations without data payload.

    Used for operations that only need to confirm success with a message.

    Attributes:
        message: Human-readable success message.

    Usage:
        MessageResponse(message="Operation completed successfully")
    """
    message: str = Field(..., description="Success message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )


class HealthCheckResponse(BaseModel):
    """Health check endpoint response.

    Provides service status and metadata for monitoring.

    Attributes:
        status: Service health status (healthy/unhealthy).
        timestamp: Current server timestamp.
        service: Service name.
        version: Service version.
        mode: Running mode (development/production).
        database_status: Database connection status.
    """
    status: str = Field(..., description="Service status (healthy/unhealthy)")
    timestamp: datetime = Field(default_factory=utcnow, description="Current timestamp")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    mode: str = Field(..., description="Running mode (development/production)")
    database_status: str = Field(..., description="Database connection status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "timestamp": "2025-11-17T12:00:00+00:00",
                "service": "DataRails Demo API",
                "version": "0.1.0",
                "mode": "development",
                "database_status": "connected"
            }
        }
    )


class BadRequestError(ErrorDetail):
    """400 Bad Request error detail.

    Used when request is malformed or contains invalid data.
    """
    error_code: str = Field(default="BAD_REQUEST")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Invalid file format. Expected .xlsx",
                "error_code": "BAD_REQUEST"
            }
        }
    )


class UnauthorizedError(ErrorDetail):
    """401 Unauthorized error detail.

    Used when authentication is missing or invalid.
    """
    error_code: str = Field(default="UNAUTHORIZED")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Could not validate credentials",
                "error_code": "UNAUTHORIZED"
            }
        }
    )


class ForbiddenError(ErrorDetail):
    """403 Forbidden error detail.

    Used when user is authenticated but lacks required permissions.
    """
    error_code: str = Field(default="FORBIDDEN")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "You don't have permission to access this resource",
                "error_code": "FORBIDDEN"
            }
        }
    )


class NotFoundError(ErrorDetail):
    """404 Not Found error detail.

    Used when requested resource does not exist.
    """
    error_code: str = Field(default="NOT_FOUND")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Resource not found",
                "error_code": "NOT_FOUND"
            }
        }
    )


class ConflictError(ErrorDetail):
    """409 Conflict error detail.

    Used when request conflicts with current resource state.
    """
    error_code: str = Field(default="CONFLICT")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Resource already exists",
                "error_code": "CONFLICT"
            }
        }
    )


class RateLimitExceededError(ErrorDetail):
    """429 Rate Limit Exceeded error detail.

    Used when client exceeds rate limit.
    """
    error_code: str = Field(default="RATE_LIMIT_EXCEEDED")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Too many requests. Please try again later.",
                "error_code": "RATE_LIMIT_EXCEEDED"
            }
        }
    )


class InternalServerError(ErrorDetail):
    """500 Internal Server Error detail.

    Used when an unexpected error occurs on the server.
    """
    error_code: str = Field(default="INTERNAL_SERVER_ERROR")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "An unexpected error occurred",
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        }
    )


class ServiceUnavailableError(ErrorDetail):
    """503 Service Unavailable error detail.

    Used when service or dependency is temporarily unavailable.
    """
    error_code: str = Field(default="SERVICE_UNAVAILABLE")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Database connection unavailable",
                "error_code": "SERVICE_UNAVAILABLE"
            }
        }
    )


class BadRequestErrorResponse(BaseErrorResponse):
    """Complete 400 Bad Request response."""
    error: BadRequestError = Field(...)


class UnauthorizedErrorResponse(BaseErrorResponse):
    """Complete 401 Unauthorized response."""
    error: UnauthorizedError = Field(...)


class ForbiddenErrorResponse(BaseErrorResponse):
    """Complete 403 Forbidden response."""
    error: ForbiddenError = Field(...)


class NotFoundErrorResponse(BaseErrorResponse):
    """Complete 404 Not Found response."""
    error: NotFoundError = Field(...)


class ConflictErrorResponse(BaseErrorResponse):
    """Complete 409 Conflict response."""
    error: ConflictError = Field(...)


class ValidationErrorResponse(BaseErrorResponse):
    """Complete 422 Unprocessable Entity response."""
    error: ValidationErrorDetail = Field(...)


class RateLimitExceededErrorResponse(BaseErrorResponse):
    """Complete 429 Rate Limit Exceeded response."""
    error: RateLimitExceededError = Field(...)


class InternalServerErrorResponse(BaseErrorResponse):
    """Complete 500 Internal Server Error response."""
    error: InternalServerError = Field(...)


class ServiceUnavailableErrorResponse(BaseErrorResponse):
    """Complete 503 Service Unavailable response."""
    error: ServiceUnavailableError = Field(...)


def get_error_code(status_code: int) -> str:
    """Map HTTP status code to machine-readable error code.

    Args:
        status_code: HTTP status code (e.g., 404, 500).

    Returns:
        Machine-readable error code string.
        Returns "UNKNOWN_ERROR" for unmapped codes.

    Example:
        error_code = get_error_code(404)  # Returns "NOT_FOUND"
    """
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
        503: "SERVICE_UNAVAILABLE"
    }
    return error_codes.get(status_code, "UNKNOWN_ERROR")


# Rebuild models to resolve forward references
BaseErrorResponse.model_rebuild()
