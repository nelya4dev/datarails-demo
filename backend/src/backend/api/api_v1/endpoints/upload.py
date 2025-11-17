"""Upload API endpoints for file processing."""

import math
import uuid
from pathlib import Path as FilePath
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Query, Path
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.db.session import get_db
from backend.crud.upload_job_crud import upload_job_crud
from backend.schemas.upload_job import (
    UploadJobCreate,
    UploadJobInDB,
    UploadJobResponse
)
from backend.schemas.common import (
    BaseResponse,
    BaseErrorResponse,
    PaginatedResponse
)
from backend.tasks.process_upload import process_upload_task

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = {".xlsx", ".xls"}
UPLOAD_PATH = settings.UPLOAD_DIR_ABSOLUTE_PATH

# Ensure upload directory exists
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)


def validate_file_extension(filename: str) -> None:
    """Validate file has allowed extension."""
    file_ext = FilePath(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format. Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed."
        )


async def validate_file_size(file: UploadFile) -> None:
    """Validate file size is within limits."""
    contents = await file.read()
    file_size = len(contents)
    await file.seek(0)

    if file_size > settings.UPLOAD_MAX_FILE_SIZE:
        max_size_mb = settings.UPLOAD_MAX_FILE_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {max_size_mb}MB."
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty."
        )


async def save_upload_file(file: UploadFile) -> tuple[str, str]:
    """Save uploaded file to disk with unique filename.

    Returns:
        Tuple of (original_filename, saved_filename_only).
    """
    try:
        file_id = uuid.uuid4()
        file_ext = FilePath(file.filename).suffix
        safe_filename = f"{file_id}{file_ext}"
        file_path = UPLOAD_PATH / safe_filename

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return file.filename, safe_filename  # Return only filename, not full path

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )


@router.post(
    "",
    response_model=BaseResponse[UploadJobResponse],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload Excel file for processing"
)
async def upload_file(
        request: Request,
        file: UploadFile = File(..., description="Excel file (.xlsx or .xls)"),
        db: Session = Depends(get_db)
) -> BaseResponse[UploadJobResponse]:
    """Upload Excel file for asynchronous processing."""
    try:
        validate_file_extension(file.filename)
        await validate_file_size(file)

        original_filename, saved_filename = await save_upload_file(file)

        job_data = UploadJobCreate(
            filename=original_filename,
            file_path=saved_filename  # Store only filename
        )
        upload_job = upload_job_crud.create(db, obj_in=job_data)

        request.state.job_id = str(upload_job.id)

        # Trigger Celery task
        process_upload_task.delay(str(upload_job.id), saved_filename)

        response_data = UploadJobResponse(
            job_id=str(upload_job.id),
            message="File uploaded successfully. Processing started."
        )

        return BaseResponse[UploadJobResponse](
            success=True,
            data=response_data
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process upload: {str(e)}"
        )


@router.get(
    "/jobs",
    response_model=BaseResponse[PaginatedResponse[UploadJobInDB]],
    status_code=status.HTTP_200_OK,
    summary="Get upload jobs list"
)
async def get_upload_jobs(
        page: int = Query(default=1, ge=1),
        size: int = Query(default=20, ge=1, le=100),
        status: Optional[str] = Query(default=None),
        db: Session = Depends(get_db)
) -> BaseResponse[PaginatedResponse[UploadJobInDB]]:
    """Get paginated list of upload jobs."""
    try:
        skip = (page - 1) * size
        filters = {"status": status} if status else None

        jobs = upload_job_crud.get_jobs_ordered(db, filters=filters, skip=skip, limit=size)
        total = upload_job_crud.count_with_filter(db, filters=filters)
        items = [UploadJobInDB.model_validate(job) for job in jobs]
        pages = math.ceil(total / size) if total > 0 else 0

        paginated_data = PaginatedResponse[UploadJobInDB](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

        return BaseResponse[PaginatedResponse[UploadJobInDB]](
            success=True,
            data=paginated_data
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve upload jobs: {str(e)}"
        )


@router.get(
    "/status/{job_id}",
    response_model=BaseResponse[UploadJobInDB],
    status_code=status.HTTP_200_OK,
    summary="Get upload job status"
)
async def get_upload_job_status(
        job_id: str = Path(...),
        db: Session = Depends(get_db)
) -> BaseResponse[UploadJobInDB]:
    """Get detailed status of a specific upload job."""
    try:
        try:
            job_uuid = uuid.UUID(job_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid job_id format. Expected UUID, got: {job_id}"
            )

        job = upload_job_crud.get(db, id_value=job_uuid)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Upload job with ID {job_id} not found"
            )

        job_data = UploadJobInDB.model_validate(job)

        return BaseResponse[UploadJobInDB](
            success=True,
            data=job_data
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve job status: {str(e)}"
        )
