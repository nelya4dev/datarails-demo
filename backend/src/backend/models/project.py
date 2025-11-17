"""Project model with source data and transformed fields."""

from typing import Optional
from uuid import UUID, uuid4
from datetime import date

from sqlalchemy import String, Float, Date, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from backend.db.base_class import Base
from backend.db.lengths import L
from backend.models.model_mixin import TimestampMixin


class Project(TimestampMixin, Base):
    """Project model storing both source data and transformed fields.

    Stores ALL columns from Excel Projects sheet:
    - Source data: As-is from Excel (project_id, project_name, budget_usd, start_date, status)
    - Transformed data: Calculated/mapped values (if any from config.csv)

    The config.csv defines transformation rules for specific fields, but we store
    both original and transformed values for audit trail and flexibility.

    Attributes:
        id: Internal UUID primary key

        Source Data (from Excel - EXACT column names):
        project_id: Project ID from Excel (business key)
        project_name: Project name
        budget_usd: Budget amount in USD from Excel
        start_date: Project start date
        status: Project status (e.g., "Active", "Complete", "On Hold", "Pending")

        Transformed Data (from config.csv rules - if any):
        (Currently no transformations, but structure allows for future additions)

    Indexes:
        - project_id (unique business key)
        - status (for filtering)

    Table name: project (auto-generated from class name)
    """

    # Internal ID
    id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)

    # Source + Transform
    project_id: Mapped[str] = mapped_column(
        String(L.CODE),
        nullable=False,
        comment="Project ID from Excel (business key)"
    )

    project_name: Mapped[Optional[str]] = mapped_column(
        String(L.TITLE),
        nullable=True,
        comment="Project name from Excel"
    )

    budget_usd: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Budget amount in USD from Excel"
    )

    start_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Project start date from Excel"
    )

    status: Mapped[Optional[str]] = mapped_column(
        String(L.CODE),
        nullable=True,
        comment="Project status from Excel (Active, Complete, On Hold, Pending)"
    )

    __table_args__ = (
        Index('ix_project_project_id', 'project_id', unique=True),
        Index('ix_project_status', 'status'),
    )

    def __repr__(self) -> str:
        return (
            f"<Project id={self.id!r} "
            f"project_id={self.project_id!r} "
            f"name={self.project_name!r} "
            f"status={self.status!r}>"
        )
