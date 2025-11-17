import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api.api_v1.api import api_router
from backend.core.config import settings
from backend.schemas.common import (
    get_error_code,
    HealthCheckResponse,
    BaseErrorResponse,
    ErrorDetail,
    ValidationErrorDetail,
    ValidationErrorItem
)
from backend.db.session import test_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Suppress passlib bcrypt warnings (noisy in logs)
logging.getLogger('passlib').setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler for startup and shutdown.

    Manages application lifecycle events using async context manager pattern.
    Logs startup and shutdown events for monitoring and debugging.

    Startup Events:
        - Log application mode (development/production)
        - Log database connection info
        - Test database connection
        - Log startup complete

    Shutdown Events:
        - Close database connections
        - Cleanup background tasks
        - Log shutdown complete

    Args:
        app: FastAPI application instance.

    Yields:
        Control to application (runs between startup and shutdown).
    """
    # Startup
    logger.info(f"Starting DataRails Demo API in {settings.APP_MODE} mode")
    logger.info(f"Database URL configured for host: {settings.DB_HOST}")

    # Test database connection
    try:
        test_connection()
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down DataRails Demo API")
    logger.info("Application shutdown complete")


# ==================== EXCEPTION HANDLERS ====================
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with wrapped error response format.

    Catches all HTTPException instances raised by endpoints and formats them
    with BaseErrorResponse structure for consistency.

    Args:
        request: FastAPI request object.
        exc: HTTP exception with status_code and detail.

    Returns:
        JSONResponse with wrapped error format:
        {
            "success": false,
            "error": {
                "detail": "Error message",
                "error_code": "NOT_FOUND"
            }
        }

    Side Effects:
        Logs warning with status code, URL, and error detail.
    """
    logger.warning(f"HTTP {exc.status_code} on {request.url}: {exc.detail}")

    # Create wrapped error response
    error_response = BaseErrorResponse(
        success=False,
        error=ErrorDetail(
            detail=str(exc.detail),
            error_code=get_error_code(exc.status_code)
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
        headers=getattr(exc, 'headers', None)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with wrapped field-level error details.

    Catches RequestValidationError (raised when request body/params fail Pydantic
    validation) and formats errors with BaseErrorResponse structure.

    Args:
        request: FastAPI request object.
        exc: Validation error with list of field errors.

    Returns:
        JSONResponse with 422 status and wrapped validation errors:
        {
            "success": false,
            "error": {
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

    Side Effects:
        Logs error with URL and validation error details.
    """
    logger.error(f"Validation error on {request.url}: {exc.errors()}")

    validation_errors = []
    for error in exc.errors():
        validation_errors.append(
            ValidationErrorItem(
                loc=list(error.get("loc", [])),
                msg=error.get("msg", ""),
                type=error.get("type", "")
            )
        )

    # Create wrapped error response
    error_response = BaseErrorResponse(
        success=False,
        error=ValidationErrorDetail(
            detail=validation_errors,
            error_code="VALIDATION_ERROR"
        )
    )

    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with wrapped 500 response.

    Catches all unhandled exceptions and returns wrapped error response.
    In development, includes exception message for debugging.
    In production, returns generic message to avoid leaking internal details.

    Args:
        request: FastAPI request object.
        exc: Unhandled exception.

    Returns:
        JSONResponse with 500 status and wrapped error:
        {
            "success": false,
            "error": {
                "detail": "Internal server error",
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        }

    Side Effects:
        Logs error with URL, exception, and full traceback.
    """
    logger.error(f"Unexpected error on {request.url}: {exc}", exc_info=True)

    # Create wrapped error response
    error_message = str(exc) if settings.is_development else "Internal server error"
    error_response = BaseErrorResponse(
        success=False,
        error=ErrorDetail(
            detail=error_message,
            error_code="INTERNAL_SERVER_ERROR"
        )
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


# ==================== FASTAPI APP ====================
app = FastAPI(
    title="DataRails Demo API",
    version="0.1.0",
    description="Data ingestion and transformation service for Excel files",
    openapi_url=f"{settings.API_PATH}/openapi.json",
    # Security: Disable API documentation in production
    # - Development: /docs and /redoc available for interactive API testing
    # - Production: Routes return 404 (not registered at all)
    docs_url=f"{settings.API_PATH}/docs" if settings.is_development else None,
    redoc_url=f"{settings.API_PATH}/redoc" if settings.is_development else None,
    lifespan=lifespan
)

# ==================== EXCEPTION HANDLERS ====================
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ==================== SECURITY MIDDLEWARE ====================
# Add TrustedHostMiddleware in production with configured hosts
# Protects against Host header injection attacks
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts_list
    )

# ==================== CORS MIDDLEWARE ====================
if settings.CORS_ALLOW_ALL_ORIGINS:
    origins = ["*"]
else:
    origins = settings.cors_origins_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== REQUEST LOGGING ====================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing information."""
    start_time = datetime.now(timezone.utc)

    response = await call_next(request)

    process_time = (datetime.now(timezone.utc) - start_time).total_seconds()
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )

    return response


# ==================== ROUTERS ====================
app.include_router(api_router, prefix=settings.API_PATH)


# ==================== HEALTH CHECK ====================
@app.get(
    "/",
    tags=["health"],
    response_model=HealthCheckResponse,
    summary="Health check endpoint",
    description="Check if the API service is running and database is connected"
)
async def health_check() -> Dict[str, Any]:
    """Health check endpoint.

    Returns service status and database connection status.
    Used by load balancers and monitoring tools to verify service health.
    """
    # Test database connection
    database_status = "disconnected"
    try:
        test_connection()
        database_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        database_status = "disconnected"

    # Determine overall status
    status = "healthy" if database_status == "connected" else "unhealthy"

    return {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "DataRails Demo API",
        "version": "0.1.0",
        "mode": settings.APP_MODE,
        "database_status": database_status
    }
