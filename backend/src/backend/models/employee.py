"""Employee model with source data and transformed fields."""

from typing import Optional
from uuid import UUID, uuid4
from datetime import date

from sqlalchemy import String, Integer, Float, Date, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from backend.db.base_class import Base
from backend.db.lengths import L
from backend.models.model_mixin import TimestampMixin


class Employee(TimestampMixin, Base):
    """Employee model storing both source data and transformed fields.

    Stores ALL columns from Excel Employees sheet:
    - Source data: As-is from Excel (employee_id, name, department_code, salary, hire_date)
    - Transformed data: Calculated/mapped values (department_name, annual_salary_eur, tenure_years)

    The config.csv defines transformation rules for specific fields, but we store
    both original and transformed values for audit trail and flexibility.

    Attributes:
        id: Internal UUID primary key

        Source Data (from Excel - EXACT column names):
        employee_id: Employee ID from Excel (business key)
        name: Employee full name
        department_code: Department code (e.g., "HR", "DEV", "FIN", "MKT")
        salary: Original salary amount from Excel
        hire_date: Employee hire date from Excel

        Transformed Data (from config.csv rules):
        department_name: Human-readable department name (mapped from department_code)
        annual_salary_eur: Calculated salary in EUR (converted from salary)
        tenure_years: Calculated years of service (from hire_date)

    Indexes:
        - employee_id (unique business key)
        - department_code (for filtering)
        - department_name (for filtering)

    Table name: employee (auto-generated from class name)
    """

    # Internal ID
    id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)

    # Source
    employee_id: Mapped[str] = mapped_column(
        String(L.CODE),
        nullable=False,
        comment="Employee ID from Excel (business key)"
    )

    name: Mapped[Optional[str]] = mapped_column(
        String(L.NAME_FULL),
        nullable=True,
        comment="Employee full name from Excel"
    )

    department_code: Mapped[Optional[str]] = mapped_column(
        String(L.CODE),
        nullable=True,
        comment="Department code from Excel (e.g., 'HR', 'DEV', 'FIN', 'MKT')"
    )

    salary: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Original salary amount from Excel"
    )

    hire_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Employee hire date from Excel"
    )

    # Transformed
    department_name: Mapped[Optional[str]] = mapped_column(
        String(L.TITLE),
        nullable=True,
        comment="Transformed department name (mapped from department_code via config.csv)"
    )

    annual_salary_eur: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Transformed annual salary in EUR (calculated from salary via config.csv)"
    )

    tenure_years: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Calculated years of service (from hire_date)"
    )

    __table_args__ = (
        Index('ix_employee_employee_id', 'employee_id', unique=True),
        Index('ix_employee_department_code', 'department_code'),
        Index('ix_employee_department_name', 'department_name'),
    )

    def __repr__(self) -> str:
        return (
            f"<Employee id={self.id!r} "
            f"employee_id={self.employee_id!r} "
            f"name={self.name!r} "
            f"department={self.department_name!r}>"
        )
