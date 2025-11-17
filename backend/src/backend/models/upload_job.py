from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, Index, Integer, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from backend.db.base_class import Base
from backend.db.lengths import L
from backend.models.model_mixin import TimestampMixin


class UploadJob(TimestampMixin, Base):
    """Upload job tracking model for async file processing.

    Tracks the lifecycle of an Excel file upload from submission through
    processing to completion or failure. Used to provide real-time status
    updates to the frontend.

    Status flow:
        pending → processing → completed
                            ↘ failed

    Attributes:
        id: Internal UUID primary key
        filename: Original filename of uploaded Excel file
        file_path: Server path where file is stored temporarily
        status: Current processing status (pending/processing/completed/failed)
        current_step: Current processing step (reading/validating/transforming/persisting)
        total_rows: Total number of rows across all sheets
        processed_rows: Number of rows successfully processed
        error_rows: Number of rows that failed validation/transformation
        error_details: JSON array of error objects with row/field/message
        error_message: Overall error message if job failed completely
        started_at: When processing actually began (not when job was created)
        completed_at: When processing finished (success or failure)

    Table name: upload_job (auto-generated from class name)
    """

    id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    filename: Mapped[str] = mapped_column(String(L.PATH), nullable=False)
    file_path: Mapped[str] = mapped_column(String(L.PATH), nullable=False)
    status: Mapped[str] = mapped_column(String(L.CODE), nullable=False, default="pending")
    current_step: Mapped[Optional[str]] = mapped_column(String(L.CODE), nullable=True)
    total_rows: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    processed_rows: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    error_rows: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    error_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        Index('ix_upload_job_status', 'status'),
        Index('idx_upload_job_status_created', 'status', 'created_at'),
    )

    def __repr__(self) -> str:
        return (
            f"<UploadJob id={self.id!r} "
            f"status={self.status!r} filename={self.filename!r}>"
        )
